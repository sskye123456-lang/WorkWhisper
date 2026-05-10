"""
职场嘴替 - 飞书事件处理器
"""
import json
import hashlib
from typing import Optional
from fastapi import Request

from app.config import config
from app.models.user import User, UserState, PersonaType, PERSONAS
from app.services.database import db
from app.services.llm import llm_service
from app.cards.builder import card_builder
from app.quiz.questions import get_question, calculate_persona_scores, get_dominant_persona, QUIZ_QUESTIONS


class FeishuHandler:
    """飞书事件处理器"""
    
    def __init__(self):
        self.verification_token = config.FEISHU_APP_ID
    
    def verify_signature(self, request: Request, body: bytes) -> bool:
        """验证飞书请求签名"""
        # 简化版本，实际需要验证签名
        return True
    
    async def handle_event(self, event: dict) -> Optional[dict]:
        """处理飞书事件"""
        event_type = event.get("type")
        
        # URL验证
        if event_type == "url_verification":
            return {"challenge": event.get("challenge")}
        
        # 消息事件
        if event_type == "event_callback":
            return await self._handle_message_event(event.get("event", {}))
        
        # 卡片回调
        if event_type == "card":
            return await self._handle_card_callback(event)
        
        return None
    
    async def _handle_message_event(self, event: dict) -> Optional[dict]:
        """处理消息事件"""
        sender = event.get("sender", {})
        open_id = sender.get("sender_id", {}).get("open_id", "")
        
        if not open_id:
            return None
        
        message = event.get("message", {})
        msg_type = message.get("msg_type")
        content = message.get("content", "")
        
        # 获取或创建用户
        user = db.get_user(open_id)
        if not user:
            user = db.create_user(open_id)
        
        # 处理不同消息类型
        if msg_type == "text":
            text = json.loads(content).get("text", "") if isinstance(content, str) else content
            return await self._handle_text_message(user, text)
        
        elif msg_type == "image":
            # TODO: OCR处理
            return card_builder.simple_text_card("📷 已收到截图，正在识别中...", "blue")
        
        elif msg_type == "post":
            # 转发的消息
            return await self._handle_forward_message(user, content)
        
        return None
    
    async def _handle_text_message(self, user: User, text: str) -> dict:
        """处理文本消息"""
        text = text.strip()
        
        # 快捷指令处理
        if text in ["帮助", "怎么用", "说明", "help"]:
            return card_builder.help_card()
        
        if text in ["换人设", "切换人设", "switch"]:
            return card_builder.persona_select_card(user.current_persona)
        
        if text in ["请外援", "外援", "reinforcement"]:
            if not user.current_persona:
                return card_builder.simple_text_card("🤔 你还没有选择人设，请先选择一个人设！", "orange")
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
                return card_builder.simple_text_card(f"当前人设：{p.emoji} {p.title}\n\"{p.quote}\"", p.header_template)
            return card_builder.simple_text_card("你还没有选择人设", "orange")
        
        # 根据用户状态处理
        if user.state == UserState.NEW:
            # 新用户，引导选择人设
            return card_builder.welcome_card()
        
        if user.state == UserState.IN_QUIZ:
            # 正在做测试，忽略非选项消息
            question = get_question(user.quiz_progress + 1)
            if question:
                return card_builder.quiz_card(question, user.quiz_progress)
            return card_builder.welcome_card()
        
        if user.state == UserState.HAS_PERSONA or user.state == UserState.WAITING_REPLY:
            # 已有人设，生成回复
            if not user.current_persona:
                return card_builder.persona_select_card()
            
            # 调用LLM生成回复
            suggestion = llm_service.generate_reply(user.current_persona, text)
            remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
            
            return card_builder.reply_card(suggestion, text, remaining)
        
        return card_builder.welcome_card()
    
    async def _handle_forward_message(self, user: User, content: dict) -> dict:
        """处理转发消息"""
        # 解析转发的内容
        # TODO: 实际解析飞书转发消息格式
        return card_builder.simple_text_card("📨 已收到转发的对话，正在处理中...", "blue")
    
    async def _handle_card_callback(self, event: dict) -> Optional[dict]:
        """处理卡片回调"""
        action = event.get("action", {})
        value = action.get("value", {})
        
        open_id = event.get("open_id", "")
        if not open_id:
            return None
        
        user = db.get_user(open_id)
        if not user:
            user = db.create_user(open_id)
        
        action_type = value.get("action")
        
        # 开始测试
        if action_type == "start_quiz":
            user.state = UserState.IN_QUIZ
            user.quiz_progress = 0
            user.quiz_answers = []
            db.update_user(user)
            question = get_question(1)
            return card_builder.quiz_card(question, 0)
        
        # 答题
        if action_type == "answer":
            question_id = value.get("question_id", 1)
            answer = value.get("answer", "A")
            
            # 保存答案
            user = db.save_quiz_answer(open_id, question_id, answer)
            
            # 检查是否完成
            if question_id >= len(QUIZ_QUESTIONS):
                # 计算结果
                scores = calculate_persona_scores(user.quiz_answers)
                dominant = get_dominant_persona(scores)
                
                user.state = UserState.HAS_PERSONA
                user.current_persona = dominant
                db.update_user(user)
                
                return card_builder.quiz_result_card(dominant, scores)
            
            # 继续下一题
            question = get_question(question_id + 1)
            return card_builder.quiz_card(question, question_id)
        
        # 选择人设
        if action_type == "select_persona":
            persona_str = value.get("persona")
            if persona_str:
                persona = PersonaType(persona_str)
                user = db.set_persona(open_id, persona)
                p = PERSONAS[persona]
                return card_builder.simple_text_card(
                    f"✅ 已切换到【{p.emoji} {p.title}】\n\n\"{p.quote}\"\n\n从现在开始，我会用这个人设帮你回复。💬 把同事的消息发给我吧！",
                    p.header_template
                )
            return card_builder.persona_select_card()
        
        # 确认人设（测试结果后）
        if action_type == "confirm_persona":
            persona_str = value.get("persona")
            if persona_str:
                persona = PersonaType(persona_str)
                user = db.set_persona(open_id, persona)
                p = PERSONAS[persona]
                return card_builder.simple_text_card(
                    f"✅ 已选择【{p.emoji} {p.title}】\n\n💬 把同事的消息发给我，我帮你回复！",
                    p.header_template
                )
            return card_builder.welcome_card()
        
        # 请外援
        if action_type == "call_reinforcement":
            if not user.current_persona:
                return card_builder.persona_select_card()
            
            # 检查是否有指定人设
            persona_str = value.get("persona")
            if persona_str:
                target_persona = PersonaType(persona_str)
                
                # 检查次数
                user, success = db.use_reinforcement(open_id)
                if not success:
                    return card_builder.reinforcement_exhaust_card()
                
                # TODO: 需要原始消息才能生成回复
                return card_builder.simple_text_card(
                    f"🆘 已呼叫【{PERSONAS[target_persona].emoji} {PERSONAS[target_persona].title}】外援！\n\n请重新发送同事的消息，我将用外援人设帮你回复。",
                    "purple"
                )
            
            # 显示选择列表
            remaining = user.get_reinforcement_remaining(config.REINFORCEMENT_DAILY_LIMIT)
            return card_builder.reinforcement_select_card(user.current_persona, remaining)
        
        # 换人设
        if action_type == "switch_persona":
            return card_builder.persona_select_card(user.current_persona)
        
        # 复制
        if action_type == "copy":
            # 飞书会自动处理复制，这里不需要返回
            return None
        
        # 帮助
        if action_type == "help":
            return card_builder.help_card()
        
        return None


# 全局事件处理器
feishu_handler = FeishuHandler()
