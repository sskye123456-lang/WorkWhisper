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
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, timeout=10)
            data = resp.json()
            print("DEBUG: Token response code =", data.get("code"))
            
            if data.get("code") == 0:
                self._token = data.get("tenant_access_token", "")
            else:
                print("DEBUG: Token failed:", data)
                self._token = ""
        
        return self._token

    async def send_msg(self, open_id: str, card: dict) -> bool:
        token = await self.get_token()
        if not token:
            return False
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        payload = {"receive_id": open_id, "msg_type": "interactive", "content": json.dumps(card)}
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=15)
            data = resp.json()
            if data.get("code") != 0:
                print("DEBUG: Send failed:", data.get("code"), data.get("msg"))
            return data.get("code") == 0

    async def handle_event(self, event: dict) -> Optional[dict]:
        # URL verification
        if event.get("type") == "url_verification":
            return {"challenge": event.get("challenge")}
        
        # Card callback - 飞书卡片回调会包含 action.operator.open_id
        if event.get("action") or event.get("type") == "card":
            await self._handle_card_callback(event)
            return None
        
        # Message event (v2 format)
        header = event.get("header", {})
        event_type = header.get("event_type", "")
        
        if event_type == "im.message.receive_v1":
            event_data = event.get("event", {})
            await self._on_message(event_data)
        
        return None

    async def _on_message(self, ev: dict):
        sender = ev.get("sender", {})
        sender_id = sender.get("sender_id", {})
        open_id = sender_id.get("open_id", "")
        
        if not open_id:
            return
        
        message = ev.get("message", {})
        msg_type = message.get("message_type") or message.get("msg_type")
        content = message.get("content", "")
        
        # Get or create user
        user = db.get_user(open_id)
        if not user:
            user = db.create_user(open_id)
        
        card = None
        
        if msg_type == "text":
            try:
                text = json.loads(content).get("text", "") if isinstance(content, str) else content
            except:
                text = str(content)
            card = await self._handle_text(user, text)
        else:
            card = card_builder.simple_text_card("\u6682\u65e0\u6cd5\u5904\u7406\u8fd9\u79cd\u6d88\u606f\u7c7b\u578b\uff0c\u8bf7\u53d1\u9001\u6587\u5b57\u6d88\u606f", "orange")
        
        if card:
            await self.send_msg(open_id, card)

    async def _handle_text(self, user: User, text: str) -> dict:
        text = text.strip()
        
        if text.lower() in ["help", "\u5e2e\u52a9", "\u7528\u6cd5", "\u5148\u770b\u770b\u7528\u6cd5"]:
            return card_builder.help_card()
        
        if text in ["\u5f00\u59cb\u6d4b\u8bd5", "quiz"]:
            user.state = UserState.IN_QUIZ
            user.quiz_progress = 0
            user.quiz_answers = []
            db.update_user(user)
            return card_builder.quiz_card(get_question(1), 0)
        
        if text.lower() in ["switch", "\u6362\u4eba\u8bbe", "\u5207\u6362\u4eba\u8bbe"]:
            return card_builder.persona_select_card(user.current_persona)
        
        if text in ["\u8bf7\u5916\u63f4", "\u5916\u63f4"]:
            if not user.current_persona:
                return card_builder.persona_select_card()
            remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
            return card_builder.reinforcement_select_card(user.current_persona, remaining)
        
        if text.lower() in ["test", "\u91cd\u65b0\u6d4b\u8bd5", "\u518d\u6d4b\u4e00\u6b21"]:
            user.state = UserState.IN_QUIZ
            user.quiz_progress = 0
            user.quiz_answers = []
            db.update_user(user)
            return card_builder.quiz_card(get_question(1), 0)
        
        # State machine
        if user.state == UserState.NEW:
            return card_builder.welcome_card()
        
        if user.state == UserState.IN_QUIZ:
            q = get_question(user.quiz_progress + 1)
            if q:
                return card_builder.quiz_card(q, user.quiz_progress)
            scores = calculate_persona_scores(user.quiz_answers)
            persona = get_dominant_persona(scores)
            user.state = UserState.HAS_PERSONA
            user.current_persona = persona
            db.update_user(user)
            return card_builder.quiz_result_card(persona, scores)
        
        if user.state == UserState.HAS_PERSONA:
            if not user.current_persona:
                return card_builder.persona_select_card()
            suggestion = llm_service.generate_reply(user.current_persona, text)
            remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
            return card_builder.reply_card(suggestion, text, remaining)
        
        return card_builder.welcome_card()

    async def _handle_card_callback(self, event: dict):
        print("DEBUG: card callback received, event keys:", list(event.keys()))
        
        action = event.get("action", {})
        value = action.get("value", {})
        
        # open_id 可能在多个位置，兼容不同格式
        open_id = (
            event.get("open_id", "")
            or (event.get("operator", {}).get("open_id", "") if isinstance(event.get("operator"), dict) else "")
            or (event.get("sender", {}).get("sender_id", {}).get("open_id", "") if isinstance(event.get("sender"), dict) else "")
        )
        
        print("DEBUG: extracted open_id =", open_id[:10] + "..." if open_id else "(empty)")
        
        if not open_id:
            print("DEBUG: no open_id in callback, full event:", json.dumps(event, ensure_ascii=False)[:500])
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
                    p = PERSONAS[persona]
                    card = card_builder.simple_text_card(
                        "\u2728 已选定 " + p.emoji + " " + p.title + " 作为你的职场嘴替！\n\n把同事的消息发给我，我就帮你回复～",
                        "blue"
                    )
                except Exception as e:
                    print("DEBUG: confirm_persona error:", e)
                    card = card_builder.persona_select_card()

        elif action_type == "want_counterattack":
            # 用户想逆袭体验另一种人格，弹出选择卡片
            if user.current_persona:
                card = card_builder.counterattack_select_card(user.current_persona)
            else:
                card = card_builder.persona_select_card()

        elif action_type == "counterattack_select":
            # 逆袭选择：用户选定一种人格作为默认
            p_str = value.get("persona")
            if p_str:
                try:
                    persona = PersonaType(p_str)
                    user = db.set_persona(open_id, persona)
                    p = PERSONAS[persona]
                    card = card_builder.simple_text_card(
                        "\ud83d\ude80 逆袭成功！已切换为 " + p.emoji + " " + p.title + "\n\n以后都会用这个风格帮你回复，随时发「换人设」可以重新选择～",
                        p.header_template
                    )
                except:
                    card = card_builder.persona_select_card()
        
        elif action_type == "call_reinforcement":
            p_str = value.get("persona")
            if p_str:
                user, success = db.use_reinforcement(open_id)
                if success:
                    try:
                        tp = PersonaType(p_str)
                        p = PERSONAS[tp]
                        card = card_builder.simple_text_card("\u5df2\u547c\u5524\u5916\u63f4 " + p.emoji + " " + p.title + " \uff01\u8bf7\u91cd\u65b0\u53d1\u9001\u540c\u4e8b\u7684\u6d88\u606f\u3002", "purple")
                    except:
                        pass
                else:
                    card = card_builder.reinforcement_exhaust_card()
        
        if card:
            await self.send_msg(open_id, card)


feishu_handler = FeishuHandler()
