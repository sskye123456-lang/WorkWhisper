# Feishu Handler
import json
import time
from typing import Optional, Tuple
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
        self._token: str = ""
        self._token_expire: float = 0

    async def get_token(self) -> str:
        """获取飞书 tenant_access_token，带缓存和过期机制"""
        # Token 有效期约 2 小时，提前 5 分钟刷新
        if self._token and time.time() < self._token_expire - 300:
            return self._token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, timeout=10)
                data = resp.json()
                
                if data.get("code") == 0:
                    self._token = data.get("tenant_access_token", "")
                    # expire 单位是秒，默认 7200
                    expire_in = data.get("expire", 7200)
                    self._token_expire = time.time() + expire_in
                    return self._token
                else:
                    print(f"Token failed: {data.get('code')} - {data.get('msg')}")
                    self._token = ""
                    self._token_expire = 0
                    return ""
        except Exception as e:
            print(f"Token request error: {e}")
            return ""

    async def send_msg(self, open_id: str, card: dict) -> bool:
        """发送卡片消息给用户"""
        token = await self.get_token()
        if not token:
            print("No token available")
            return False
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {
            "receive_id": open_id,
            "msg_type": "interactive",
            "content": json.dumps(card, ensure_ascii=False)
        }
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, headers=headers, timeout=15)
                data = resp.json()
                
                if data.get("code") != 0:
                    print(f"Send failed: {data.get('code')} - {data.get('msg')}")
                    # Token 过期时清空缓存
                    if data.get("code") == 99991663:  # token expired
                        self._token = ""
                        self._token_expire = 0
                    return False
                return True
        except Exception as e:
            print(f"Send request error: {e}")
            return False

    async def handle_event(self, event: dict) -> Optional[dict]:
        """处理飞书消息事件（v2 格式）"""
        # URL verification
        if event.get("type") == "url_verification":
            return {"challenge": event.get("challenge")}
        
        # 只处理消息事件
        header = event.get("header", {})
        event_type = header.get("event_type", "")
        
        if event_type == "im.message.receive_v1":
            event_data = event.get("event", {})
            await self._on_message(event_data)
        
        return None

    async def _on_message(self, ev: dict):
        """处理用户发来的消息"""
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
            except json.JSONDecodeError:
                text = str(content)
            card = await self._handle_text(user, text)
        else:
            card = card_builder.simple_text_card("暂无法处理这种消息类型，请发送文字消息", "orange")
        
        if card:
            await self.send_msg(open_id, card)

    async def _handle_text(self, user: User, text: str) -> dict:
        """根据用户输入和状态返回相应卡片"""
        text = text.strip()
        
        # 指令处理
        if text.lower() in ["help", "帮助", "用法"]:
            return card_builder.help_card()
        
        if text in ["开始测试", "quiz"]:
            return await self._start_quiz(user)
        
        if text.lower() in ["switch", "换人设", "切换人设"]:
            return card_builder.persona_select_card(user.current_persona)
        
        if text in ["请外援", "外援"]:
            return await self._handle_reinforcement(user)
        
        if text.lower() in ["test", "重新测试", "再测一次"]:
            return await self._start_quiz(user)
        
        # 状态机
        if user.state == UserState.NEW:
            return card_builder.welcome_card()
        
        if user.state == UserState.IN_QUIZ:
            return await self._continue_quiz(user)
        
        if user.state == UserState.HAS_PERSONA:
            return await self._generate_reply(user, text)
        
        return card_builder.welcome_card()

    async def _start_quiz(self, user: User) -> dict:
        """开始测试"""
        user.state = UserState.IN_QUIZ
        user.quiz_progress = 0
        user.quiz_answers = []
        db.update_user(user)
        return card_builder.quiz_card(get_question(1), 0)

    async def _continue_quiz(self, user: User) -> dict:
        """继续测试或显示结果"""
        q = get_question(user.quiz_progress + 1)
        if q:
            return card_builder.quiz_card(q, user.quiz_progress)
        
        # 测试完成，计算结果
        scores = calculate_persona_scores(user.quiz_answers)
        persona = get_dominant_persona(scores)
        user.state = UserState.HAS_PERSONA
        user.current_persona = persona
        db.update_user(user)
        return card_builder.quiz_result_card(persona, scores)

    async def _generate_reply(self, user: User, text: str) -> dict:
        """生成回复建议"""
        if not user.current_persona:
            return card_builder.persona_select_card()
        
        suggestion = llm_service.generate_reply(user.current_persona, text)
        remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
        return card_builder.reply_card(suggestion, text, remaining)

    async def _handle_reinforcement(self, user: User) -> dict:
        """处理外援请求"""
        if not user.current_persona:
            return card_builder.persona_select_card()
        remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
        return card_builder.reinforcement_select_card(user.current_persona, remaining)

    async def handle_card_callback(self, event: dict):
        """处理卡片按钮点击回调"""
        action = event.get("action", {})
        value = action.get("value", {})
        
        # 提取 open_id（飞书回调在 operator.open_id）
        open_id = ""
        operator = event.get("operator", {})
        if isinstance(operator, dict):
            open_id = operator.get("open_id", "")
        
        if not open_id:
            print(f"No open_id in callback: {list(event.keys())}")
            return
        
        # Get or create user
        user = db.get_user(open_id)
        if not user:
            user = db.create_user(open_id)
        
        action_type = value.get("action")
        
        # 路由到对应处理函数
        handlers = {
            "start_quiz": self._cb_start_quiz,
            "help": self._cb_help,
            "answer": self._cb_answer,
            "select_persona": self._cb_select_persona,
            "confirm_persona": self._cb_confirm_persona,
            "want_counterattack": self._cb_want_counterattack,
            "counterattack_select": self._cb_counterattack_select,
            "call_reinforcement": self._cb_call_reinforcement,
        }
        
        handler = handlers.get(action_type)
        if handler:
            card = await handler(user, open_id, value)
            if card:
                await self.send_msg(open_id, card)
        else:
            print(f"Unknown action: {action_type}")

    # ========== 回调处理函数 ==========
    
    async def _cb_start_quiz(self, user: User, open_id: str, value: dict) -> dict:
        """开始测试按钮"""
        user.state = UserState.IN_QUIZ
        user.quiz_progress = 0
        user.quiz_answers = []
        db.update_user(user)
        return card_builder.quiz_card(get_question(1), 0)

    async def _cb_help(self, user: User, open_id: str, value: dict) -> dict:
        """帮助按钮"""
        return card_builder.help_card()

    async def _cb_answer(self, user: User, open_id: str, value: dict) -> dict:
        """答题按钮"""
        qid = value.get("question_id", 1)
        answer = value.get("answer", "A")
        user = db.save_quiz_answer(open_id, qid, answer)
        
        if qid >= len(QUIZ_QUESTIONS):
            # 测试完成
            scores = calculate_persona_scores(user.quiz_answers)
            persona = get_dominant_persona(scores)
            user.state = UserState.HAS_PERSONA
            user.current_persona = persona
            db.update_user(user)
            return card_builder.quiz_result_card(persona, scores)
        else:
            # 下一题
            return card_builder.quiz_card(get_question(qid + 1), qid)

    async def _cb_select_persona(self, user: User, open_id: str, value: dict) -> dict:
        """选择人设按钮"""
        p_str = value.get("persona")
        if not p_str:
            return card_builder.persona_select_card()
        
        try:
            persona = PersonaType(p_str)
            user = db.set_persona(open_id, persona)
            p = PERSONAS[persona]
            return card_builder.simple_text_card(f"已切换到 {p.emoji} {p.title}", p.header_template)
        except ValueError as e:
            print(f"Invalid persona: {p_str}, error: {e}")
            return card_builder.persona_select_card()

    async def _cb_confirm_persona(self, user: User, open_id: str, value: dict) -> dict:
        """确认使用测试人格按钮"""
        p_str = value.get("persona")
        if not p_str:
            return card_builder.persona_select_card()
        
        try:
            persona = PersonaType(p_str)
            user = db.set_persona(open_id, persona)
            p = PERSONAS[persona]
            msg = f"✨ 已选定 {p.emoji} {p.title} 作为你的职场嘴替！\n\n把同事的消息发给我，我就帮你回复～"
            return card_builder.simple_text_card(msg, "blue")
        except ValueError as e:
            print(f"Invalid persona in confirm: {p_str}, error: {e}")
            return card_builder.persona_select_card()

    async def _cb_want_counterattack(self, user: User, open_id: str, value: dict) -> dict:
        """逆袭体验按钮"""
        if user.current_persona:
            return card_builder.counterattack_select_card(user.current_persona)
        else:
            return card_builder.persona_select_card()

    async def _cb_counterattack_select(self, user: User, open_id: str, value: dict) -> dict:
        """选择逆袭人格按钮"""
        p_str = value.get("persona")
        if not p_str:
            return card_builder.persona_select_card()
        
        try:
            persona = PersonaType(p_str)
            user = db.set_persona(open_id, persona)
            p = PERSONAS[persona]
            msg = f"🚀 逆袭成功！已切换为 {p.emoji} {p.title}\n\n以后都会用这个风格帮你回复，随时发「换人设」可以重新选择～"
            return card_builder.simple_text_card(msg, p.header_template)
        except ValueError as e:
            print(f"Invalid persona in counterattack: {p_str}, error: {e}")
            return card_builder.persona_select_card()

    async def _cb_call_reinforcement(self, user: User, open_id: str, value: dict) -> dict:
        """呼叫外援按钮"""
        p_str = value.get("persona")
        if not p_str:
            return None
        
        user, success = db.use_reinforcement(open_id)
        if not success:
            return card_builder.reinforcement_exhaust_card()
        
        try:
            tp = PersonaType(p_str)
            p = PERSONAS[tp]
            return card_builder.simple_text_card(f"已呼叫外援 {p.emoji} {p.title}！请重新发送同事的消息。", "purple")
        except ValueError as e:
            print(f"Invalid persona in reinforcement: {p_str}, error: {e}")
            return None


feishu_handler = FeishuHandler()
