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
        if self._tenant_access_token:
            return self._tenant_access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        
        aid_len = len(self.app_id) if self.app_id else 0
        ase_len = len(self.app_secret) if self.app_secret else 0
        print("DEBUG app_id len=" + str(aid_len) + " secret_len=" + str(ase_len))
        print("DEBUG app_id=" + str(self.app_id[:10]) + "...")
        print("DEBUG app_secret=" + str(self.app_secret[:6]) + "...")
        
        payload = {
            "app_id": self.app_id.strip
