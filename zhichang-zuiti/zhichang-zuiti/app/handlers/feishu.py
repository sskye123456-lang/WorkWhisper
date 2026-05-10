"""
职场嘴替 - 飞书事件处理器
"""
import json
import os
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
        
        # 打印调试信息（脱敏）
        app_id_display = self.app_id[:8] + "..." if self.app_id and len(self.app_id) > 8 else self.app_id
        app_secret_display = self.app_secret[:4] + "..." if self.app_secret and len(self.app_secret) > 4 else "(empty)"
        print(f"🔑 尝试获取token - app_id: {app_id_display}, app_secret: {app_secret_display}")
        print(f"🔑 app_id长度: {len(self.app_id) if self.app_id else 0}, app_secret长度: {len(self.app_secret) if self.app_secret else 0}")
        print(f"🔑 app_id repr: {repr(self.app_id)}
