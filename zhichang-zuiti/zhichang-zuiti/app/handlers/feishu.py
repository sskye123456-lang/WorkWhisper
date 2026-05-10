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

    async def get_token(self):
        if self._token:
            return self._token
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {"app_id": self.app_id, "app_secret": self.app_secret}
        async with httpx.AsyncClient() as c:
            r = await c.post(url, json=data, timeout=10)
            d = r.json()
            print("TOKEN RESP:", d)
            if d.get("code") == 0:
                self._token = d.get("tenant_access_token", "")
        return self._token

    async def send_msg(self, open_id, card):
        t = await self.get_token()
        if not t:
            print("NO TOKEN")
            return False
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        h = {"Authorization": "Bearer " + t, "Content-Type": "application/json"}
        p = {"receive_id": open_id, "msg_type": "interactive", "content": json.dumps(card)}
        async with httpx.AsyncClient() as c:
            r = await c.post(url, json=p, headers=h, timeout=15)
            d = r.json()
            print("SEND RESP:", d)
            return d.get("code") == 0

    async def handle_event(self, event):
        if event.get("type") == "url_verification":
            return {"challenge": event.get("challenge")}
        et = event.get("header", {}).get("event_type", "")
        if et == "im.message.receive_v1":
            await self._on_msg(event.get("event", {}))
        return None

    async def _on_msg(self, ev):
        oid = ev.get("sender", {}).get("sender_id", {}).get("open_id", "")
        if not oid:
            return
        msg = ev.get("message", {})
        mt = msg.get("msg_type")
        ct = msg.get("content", "")
        u = db.get_user(oid) or db.create_user(oid)
        card = None
        if mt == "text":
            txt = json.loads(ct).get("text", "") if isinstance(ct, str) else ct
            card = await self._handle_txt(u, txt)
        if card:
            await self.send_msg(oid, card)

    async def _handle_txt(self, u, txt):
        txt = txt.strip()
        if txt in ["help"]:
            return card_builder.help_card()
        if u.state == UserState.NEW:
            return card_builder.welcome_card()
        if u.state == UserState.IN_QUIZ:
            q = get_question(u.quiz_progress + 1)
            if q:
                return card_builder.quiz_card(q, u.quiz_progress)
            return card_builder.welcome_card()
        if u.state == UserState.HAS_PERSONA and u.current_persona:
            s = llm_service.generate_reply(u.current_persona, txt)
            r = u.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
            return card_builder.reply_card(s, txt, r)
        return card_builder.welcome_card()

feishu_handler = FeishuHandler()
