"""
职场嘴替 - 配置管理
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
    FEISHU_VERIFICATION_TOKEN = os.getenv("FEISHU_VERIFICATION_TOKEN", "")
    FEISHU_ENCRYPT_KEY = os.getenv("FEISHU_ENCRYPT_KEY", "")
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("PORT", os.getenv("SERVER_PORT", "10000")))
    
    REINFORCEMENT_DAILY_LIMIT = int(os.getenv("REINFORCEMENT_DAILY_LIMIT", "3"))
    ENABLE_OCR = os.getenv("ENABLE_OCR", "false").lower() == "true"
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/zhichang_zuiti.db")


config = Config()
