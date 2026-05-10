"""
Feishu Handler
"""
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
        self._tenant_access_token = ""

    async def get_tenant_access_token(self) -> str:
        if self._tenant_access_token:
            return self._tenant_access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        
        # Debug
        print("DEBUG: app_id length =", len(self.app_id) if self.app_id else 0)
        print("DEBUG: app_secret length =", len(self.app_secret) if self.app_secret else 0)
        
        # Build payload
        payload = {}
        payload["app_id"] = self.app_id.strip() if self.app_id else ""
        payload["app_secret"] = self.app_secret.strip() if self.app_secret else ""
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, timeout=10)
            data = resp.json()
            print("DEBUG: response =", data)
            
            if data.get("code") == 0:
                self._tenant_access_token = data.get("tenant_access_token", "")
                print("DEBUG: token obtained successfully")
            else:
                print("DEBUG: failed to get token:", data)
        
        return self._tenant_access_token

    async def send_message(self, open_id: str, card: dict) -> bool:
        token = await self.get_tenant_access_token()
        if not token:
            print("ERROR: no token available")
            return False
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        headers = {}
        headers["Authorization"] = "Bearer " + token
        headers["Content-Type"] = "application/json"
        
        payload = {}
        payload["receive_id"] = open_id
        payload["msg_type"] = "interactive"
        payload["content"] = json.dumps(card)
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=15)
            data = resp.json()
            if data.get("code") != 0:
                print("ERROR: send message failed:", data)
                return False
            return True

    async def handle_event(self, event: dict) -> Optional[dict]:
        event_type = event.get("type")
        
        if event_type == "url_verification":
            return {"challenge": event.get("challenge")}
        
        header = event.get("header", {})
        event_type_v2 = header.get("event_type", "")
        
        if event_type_v2 == "im.message.receive_v1":
            event_data = event.get("event", {})
            await self._handle_message_event(event_data)
            return None
        
        if event_type == "card":
            await self._handle_card_callback(event)
            return None
        
        return None

    async def _handle_message_event(self, event: dict):
        sender = event.get("sender", {})
        sender_id = sender.get("sender_id", {})
        open_id = sender_id.get("open_id", "")
        
        if not open_id:
            print("ERROR: no open_id")
            return
        
        message = event.get("message", {})
        msg_type = message.get("msg_type")
        content = message.get("content", "")
        
        user = db.get_user(open_id)
        if not user:
            user = db.create_user(open_id)
        
        card = None
        
        if msg_type == "text":
            text = json.loads(content).get("text", "") if isinstance(content, str) else content
            card = await self._handle_text_message(user, text)
        elif msg_type == "image":
            card = card_builder.simple_text_card("Image received", "blue")
        elif msg_type == "post":
            card = card_builder.simple_text_card("Post received", "blue")
        
        if card:
            await self.send_message(open_id, card)

    async def _handle_text_message(self, user, text):
        text = text.strip()
        
        if text in ["help", "帮助"]:
            return card_builder.help_card()
        
        if text in ["switch", "换人设"]:
            return card_builder.persona_select_card(user.current_persona)
        
        if user.state == UserState.NEW:
            return card_builder.welcome_card()
        
        if user.state == UserState.IN_QUIZ:
            question = get_question(user.quiz_progress + 1)
            if question:
                return card_builder.quiz_card(question, user.quiz_progress)
            return card_builder.welcome_card()
        
        if user.state == UserState.HAS_PERSONA:
            if not user.current_persona:
                return card_builder.persona_select_card()
            suggestion = llm_service.generate_reply(user.current_persona, text)
            remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
            return card_builder.reply_card(suggestion, text, remaining)
        
        return card_builder.welcome_card()

    async def _handle_card_callback(self, event: dict):
        action = event.get("action", {})
        value = action.get("value", {})
        
        open_id = event.get("open_id", "")
        if not open_id:
            return
        
        user = db.get_user(open_id)
        if not user:
            user = db.create_user(open_id)
        
        action_type = value.get("action")
        card = None
        
        if action_type == "start_quiz":
            user.state = UserState.IN_QUIZ
            user.quiz_progress = 0
            user.quiz_answers = []
            db.update_user(user)
            question = get_question(1)
            card = card_builder.quiz_card(question, 0)
        
        elif action_type == "answer":
            question_id = value.get("question_id", 1)
            answer = value.get("answer", "A")
            user = db.save_quiz_answer(open_id, question_id, answer)
            
            if question_id >= len(QUIZ_QUESTIONS):
                scores = calculate_persona_scores(user.quiz_answers)
                dominant = get_dominant_persona(scores)
                user.state = UserState.HAS_PERSONA
                user.current_persona = dominant
                db.update_user(user)
                card = card_builder.quiz_result_card(dominant, scores)
            else:
                question = get_question(question_id + 1)
                card = card_builder.quiz_card(question, question_id)
        
        elif action_type == "select_persona":
            persona_str = value.get("persona")
            if persona_str:
                persona = PersonaType(persona_str)
                user = db.set_persona(open_id, persona)
                p = PERSONAS[persona]
                msg = "Switched to " + p.emoji + " " + p.title
                card = card_builder.simple_text_card(msg, p.header_template)
            else:
                card = card_builder.persona_select_card()
        
        if card:
            await self.send_message(open_id, card)


feishu_handler = FeishuHandler()
