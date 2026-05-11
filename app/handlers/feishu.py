# Feishu Handler
import json
from typing import Optional
import httpx

from app.config import config
from app.models.user import User, UserState, PersonaType, PERSONAS
from app.services.database import db
from app.services.llm import llm_service
from app.cards.builder import card_builder
from app.quiz.questions import get_question, calculate_persona_scores, get_dominant_persona, QUIZ_QUESTIONS


class FeishuHandler:
    def __init__(self):
        self.app_id = config.FEISHU_APP_ID
        self.app_secret = config.FEISHU_APP_SECRET
        self._token = ""

    async def get_token(self) -> str:
        if self._token:
            return self._token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        
        print("DEBUG: Getting token...")
        print("DEBUG: app_id len =", len(self.app_id) if self.app_id else 0)
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, timeout=10)
            data = resp.json()
            print("DEBUG: Token response =", data)
            
            if data.get("code") == 0:
                self._token = data.get("tenant_access_token", "")
                print("DEBUG: Token obtained successfully")
            else:
                print("DEBUG: Token failed:", data)
        
        return self._token

    async def send_msg(self, open_id: str, card: dict) -> bool:
        token = await self.get_token()
        if not token:
            print("ERROR: No token available")
            return False
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        payload = {"receive_id": open_id, "msg_type": "interactive", "content": json.dumps(card)}
        
        print("DEBUG: Sending message to", open_id[:20])
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=15)
            data = resp.json()
            print("DEBUG: Send response =", data)
            return data.get("code") == 0

    async def handle_event(self, event: dict) -> Optional[dict]:
        print("DEBUG: handle_event called")
        print("DEBUG: event type =", event.get("type"))
        
        # URL verification
        if event.get("type") == "url_verification":
            return {"challenge": event.get("challenge")}
        
        # Message event
        header = event.get("header", {})
        event_type = header.get("event_type", "")
        print("DEBUG: event_type from header =", event_type)
        
        if event_type == "im.message.receive_v1":
            event_data = event.get("event", {})
            await self._on_message(event_data)
        
        return None

    async def _on_message(self, ev: dict):
        print("DEBUG: _on_message called")
        
        sender = ev.get("sender", {})
        sender_id = sender.get("sender_id", {})
        open_id = sender_id.get("open_id", "")
        
        print("DEBUG: open_id =", open_id[:20] if open_id else "None")
        
        if not open_id:
            print("ERROR: No open_id found")
            return
        
        message = ev.get("message", {})
        msg_type = message.get("msg_type")
        content = message.get("content", "")
        
        print("DEBUG: msg_type =", msg_type)
        
        # Get or create user
        user = db.get_user(open_id)
        if not user:
            user = db.create_user(open_id)
            print("DEBUG: Created new user")
        
        card = None
        
        if msg_type == "text":
            try:
                text = json.loads(content).get("text", "") if isinstance(content, str) else content
            except:
                text = str(content)
            print("DEBUG: text =", text[:50] if text else "None")
            card = await self._handle_text(user, text)
        else:
            card = card_builder.simple_text_card("\u6682\u65e0\u6cd5\u5904\u7406\u8fd9\u79cd\u6d88\u606f\u7c7b\u578b\uff0c\u8bf7\u53d1\u9001\u6587\u5b57\u6d88\u606f", "orange")
        
        if card:
            await self.send_msg(open_id, card)

    async def _handle_text(self, user: User, text: str) -> dict:
        text = text.strip()
        print("DEBUG: _handle_text, state =", user.state, "text =", text[:30])
        
        # Commands
        if text.lower() in ["help", "帮助"]:
            return card_builder.help_card()
        
        if text in ["开始测试", "开始quiz", "quiz"]:
            user.state = UserState.IN_QUIZ
            user.quiz_progress = 0
            user.quiz_answers = []
            db.update_user(user)
            return card_builder.quiz_card(get_question(1), 0)
        
        if text.lower() in ["switch", "换人设", "切换人设"]:
            return card_builder.persona_select_card(user.current_persona)
        
        if text.lower() in ["test", "重新测试", "再测一次"]:
            user.state = UserState.IN_QUIZ
            user.quiz_progress = 0
            user.quiz_answers = []
            db.update_user(user)
            return card_builder.quiz_card(get_question(1), 0)
        
        # State machine - ANY message triggers appropriate response
        if user.state == UserState.NEW:
            # New user - start quiz
            user.state = UserState.IN_QUIZ
            user.quiz_progress = 0
            user.quiz_answers = []
            db.update_user(user)
            return card_builder.quiz_card(get_question(1), 0)
        
        if user.state == UserState.IN_QUIZ:
            # Continue quiz
            q = get_question(user.quiz_progress + 1)
            if q:
                return card_builder.quiz_card(q, user.quiz_progress)
            # Quiz done, show result
            scores = calculate_persona_scores(user.quiz_answers)
            persona = get_dominant_persona(scores)
            user.state = UserState.HAS_PERSONA
            user.current_persona = persona
            db.update_user(user)
            return card_builder.quiz_result_card(persona, scores)
        
        if user.state == UserState.HAS_PERSONA:
            # Generate reply
            if not user.current_persona:
                return card_builder.persona_select_card()
            
            suggestion = llm_service.generate_reply(user.current_persona, text)
            remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
            return card_builder.reply_card(suggestion, text, remaining)
        
        # Default
        return card_builder.welcome_card()

    async def handle_card_callback(self, event: dict):
        print("DEBUG: handle_card_callback called")
        
        action = event.get("action", {})
        value = action.get("value", {})
        open_id = event.get("open_id", "")
        
        if not open_id:
            return
        
        user = db.get_user(open_id)
        if not user:
            user = db.create_user(open_id)
        
        action_type = value.get("action")
        print("DEBUG: card action =", action_type)
        
        card = None
        
        if action_type == "start_quiz":
            user.state = UserState.IN_QUIZ
            user.quiz_progress = 0
            user.quiz_answers = []
            db.update_user(user)
            card = card_builder.quiz_card(get_question(1), 0)
        
        elif action_type == "help":
            card = card_builder.help_card()
        
        elif action_type == "answer":
            qid = value.get("question_id", 1)
            answer = value.get("answer", "A")
            user = db.save_quiz_answer(open_id, qid, answer)
            
            if qid >= len(QUIZ_QUESTIONS):
                scores = calculate_persona_scores(user.quiz_answers)
                persona = get_dominant_persona(scores)
                user.state = UserState.HAS_PERSONA
                user.current_persona = persona
                db.update_user(user)
                card = card_builder.quiz_result_card(persona, scores)
            else:
                card = card_builder.quiz_card(get_question(qid + 1), qid)
        
        elif action_type == "select_persona":
            p_str = value.get("persona")
            if p_str:
                try:
                    persona = PersonaType(p_str)
                    user = db.set_persona(open_id, persona)
                    p = PERSONAS[persona]
                    card = card_builder.simple_text_card("\u5df2\u5207\u6362\u5230 " + p.emoji + " " + p.title, p.header_template)
                except:
                    card = card_builder.persona_select_card()
        
        elif action_type == "confirm_persona":
            p_str = value.get("persona")
            if p_str:
                try:
                    persona = PersonaType(p_str)
                    user = db.set_persona(open_id, persona)
                    card = card_builder.simple_text_card("\u5df2\u9009\u5b9a\uff01\u628a\u540c\u4e8b\u7684\u6d88\u606f\u53d1\u7ed9\u6211\uff0c\u6211\u5c31\u5e2e\u4f60\u56de\u590d\uff01", "blue")
                except:
                    pass
        
        elif action_type == "call_reinforcement":
            p_str = value.get("persona")
            if p_str:
                user, success = db.use_reinforcement(open_id)
                if success:
                    try:
                        tp = PersonaType(p_str)
                        p = PERSONAS[tp]
                        card = card_builder.simple_text_card("\u5df2\u547c\u5524\u5916\u63f4 " + p.emoji + " " + p.title + " \uff01\u8bf7\u91cd\u65b0\u53d1\u9001\u540c\u4e8b\u7684\u6d88\u606f\uff0c\u6211\u5c06\u7528\u5916\u63f4\u98ce\u683c\u5e2e\u4f60\u56de\u590d\u3002", "purple")
                    except:
                        pass
                else:
                    card = card_builder.reinforcement_exhaust_card()
        
        if card:
            await self.send_msg(open_id, card)


feishu_handler = FeishuHandler()
