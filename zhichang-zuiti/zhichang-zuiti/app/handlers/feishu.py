"""
职场嘴替 - 飞书事件处理器 (Fixed Version)
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
    """飞书事件处理器"""
    
    def __init__(self):
        self.app_id = config.FEISHU_APP_ID
        self.app_secret = config.FEISHU_APP_SECRET
        self._tenant_access_token = ""
    
    async def get_tenant_access_token(self) -> str:
        """获取tenant_access_token"""
        if self._tenant_access_token:
            return self._tenant_access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        
        # 调试信息
        aid_len = len(self.app_id) if self.app_id else 0
        ase_len = len(self.app_secret) if self.app_secret else 0
        print("DEBUG app_id len=" + str(aid_len) + " secret_len=" + str(ase_len))
        print("DEBUG app_id=" + str(self.app_id[:10]) + "...")
        print("DEBUG app_secret=" + str(self.app_secret[:6]) + "...")
        
        payload = dict()
        payload["app_id"] = self.app_id.strip() if self.app_id else ""
        payload["app_secret"] = self.app_secret.strip() if self.app_secret else ""
        
        async with httpx.AsyncClient() as client:
            # JSON格式
            resp = await client.post(url, json=payload, timeout=10)
            data = resp.json()
            print("DEBUG json resp=" + str(data))
            
            # 如果失败，尝试form-data格式
            if data.get("code") != 0:
                resp2 = await client.post(url, data=payload, timeout=10)
                data2 = resp2.json()
                print("DEBUG form resp=" + str(data2))
                if data2.get("code") == 0:
                    data = data2
            
            if data.get("code") == 0:
                self._tenant_access_token = data.get("tenant_access_token", "")
                print("DEBUG token OK")
            else:
                print("DEBUG token FAIL: " + str(data))
        
        return self._tenant_access_token
    
    async def send_message(self, open_id: str, card: dict) -> bool:
        """主动发送消息给用户"""
        token = await self.get_tenant_access_token()
        if not token:
            print("ERROR no token")
            return False
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        headers = dict()
        headers["Authorization"] = "Bearer " + token
        headers["Content-Type"] = "application/json"
        
        payload = dict()
        payload["receive_id"] = open_id
        payload["msg_type"] = "interactive"
        payload["content"] = json.dumps(card)
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers, timeout=15)
            data = resp.json()
            if data.get("code") != 0:
                print("ERROR send fail: " + str(data))
                return False
            return True
    
    async def handle_event(self, event: dict) -> Optional[dict]:
        """处理飞书事件"""
        event_type = event.get("type")
        
        # URL验证
        if event_type == "url_verification":
            return {"challenge": event.get("challenge")}
        
        # 飞书v2事件格式
        header = event.get("header", {})
        event_type_v2 = header.get("event_type", "")
        
        # 处理消息事件
        if event_type_v2 == "im.message.receive_v1":
            event_data = event.get("event", {})
            await self._handle_message_event(event_data)
            return None
        
        # 处理卡片回调
        if event_type == "card":
            await self._handle_card_callback(event)
            return None
        
        return None
    
    async def _handle_message_event(self, event: dict):
        """处理消息事件"""
        sender = event.get("sender", {})
        sender_id = sender.get("sender_id", {})
        open_id = sender_id.get("open_id", "")
        
        if not open_id:
            print("ERROR no open_id")
            return
        
        message = event.get("message", {})
        msg_type = message.get("msg_type")
        content = message.get("content", "")
        
        # 获取或创建用户
        user = db.get_user(open_id)
        if not user:
            user = db.create_user(open_id)
        
        card = None
        
        if msg_type == "text":
            text = json.loads(content).get("text", "") if isinstance(content, str) else content
            card = await self._handle_text_message(user, text)
        elif msg_type == "image":
            card = card_builder.simple_text_card("已收到截图，正在识别中...", "blue")
        elif msg_type == "post":
            card = card_builder.simple_text_card("已收到转发的对话，正在处理中...", "blue")
        
        if card:
            await self.send_message(open_id, card)
    
    async def _handle_text_message(self, user: User, text: str) -> Optional[dict]:
        """处理文本消息"""
        text = text.strip()
        
        # 快捷指令
        if text in ["帮助", "怎么用", "说明", "help"]:
            return card_builder.help_card()
        
        if text in ["换人设", "切换人设", "switch"]:
            return card_builder.persona_select_card(user.current_persona)
        
        if text in ["请外援", "外援", "reinforcement"]:
            if not user.current_persona:
                return card_builder.simple_text_card("你还没有选择人设，请先选择一个人设！", "orange")
            remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
            return card_builder.reinforcement_select_card(user.current_persona, remaining)
        
        if text in ["重新测试", "再测一次", "test"]:
            user.state = UserState.IN_QUIZ
            user.quiz_progress = 0
            user.quiz_answers = []
            db.update_user(user)
            question = get_question(1)
            return card_builder.quiz_card(question, 0)
        
        if text in ["当前人设", "我的人设", "persona"]:
            if user.current_persona:
                p = PERSONAS[user.current_persona]
                msg = "当前人设：" + p.emoji + " " + p.title + "\n\"" + p.quote + "\""
                return card_builder.simple_text_card(msg, p.header_template)
            return card_builder.simple_text_card("你还没有选择人设", "orange")
        
        # 根据用户状态处理
        if user.state == UserState.NEW:
            return card_builder.welcome_card()
        
        if user.state == UserState.IN_QUIZ:
            question = get_question(user.quiz_progress + 1)
            if question:
                return card_builder.quiz_card(question, user.quiz_progress)
            return card_builder.welcome_card()
        
        if user.state == UserState.HAS_PERSONA or user.state == UserState.WAITING_REPLY:
            if not user.current_persona:
                return card_builder.persona_select_card()
            
            suggestion = llm_service.generate_reply(user.current_persona, text)
            remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
            return card_builder.reply_card(suggestion, text, remaining)
        
        return card_builder.welcome_card()
    
    async def _handle_card_callback(self, event: dict):
        """处理卡片回调"""
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
                msg = "已切换到【" + p.emoji + " " + p.title + "】\n\n\"" + p.quote + "\"\n\n从现在开始，我会用这个人设帮你回复。"
                card = card_builder.simple_text_card(msg, p.header_template)
            else:
                card = card_builder.persona_select_card()
        
        elif action_type == "confirm_persona":
            persona_str = value.get("persona")
            if persona_str:
                persona = PersonaType(persona_str)
                user = db.set_persona(open_id, persona)
                p = PERSONAS[persona]
                msg = "已选择【" + p.emoji + " " + p.title + "】\n\n把同事的消息发给我，我帮你回复！"
                card = card_builder.simple_text_card(msg, p.header_template)
            else:
                card = card_builder.welcome_card()
        
        elif action_type == "call_reinforcement":
            if not user.current_persona:
                card = card_builder.persona_select_card()
            else:
                persona_str = value.get("persona")
                if persona_str:
                    target_persona = PersonaType(persona_str)
                    user, success = db.use_reinforcement(open_id)
                    if not success:
                        card = card_builder.reinforcement_exhaust_card()
                    else:
                        tp = PERSONAS[target_persona]
                        msg = "已呼叫【" + tp.emoji + " " + tp.title + "】外援！\n\n请重新发送同事的消息，我将用外援人设帮你回复。"
                        card = card_builder.simple_text_card(msg, "purple")
                else:
                    remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
                    card = card_builder.reinforcement_select_card(user.current_persona, remaining)
        
        elif action_type == "switch_persona":
            card = card_builder.persona_select_card(user.current_persona)
        
        elif action_type == "help":
            card = card_builder.help_card()
        
        if card:
            await self.send_message(open_id, card)


feishu_handler = FeishuHandler()
