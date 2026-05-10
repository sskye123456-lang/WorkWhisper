"""
职场嘴替 - 配置管理
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置"""
    
    # 飞书配置
    FEISHU_APP_ID: str = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET: str = os.getenv("FEISHU_APP_SECRET", "")
    FEISHU_VERIFICATION_TOKEN: str = os.getenv("FEISHU_VERIFICATION_TOKEN", "")
    FEISHU_ENCRYPT_KEY: str = os.getenv("FEISHU_ENCRYPT_KEY", "")
    
    # OpenAI配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # 服务配置
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8080"))
    
    # 请外援配置
    REINFORCEMENT_DAILY_LIMIT: int = int(os.getenv("REINFORCEMENT_DAILY_LIMIT", "3"))
    
    # OCR配置
    ENABLE_OCR: bool = os.getenv("ENABLE_OCR", "false").lower() == "true"
    
    # 数据库配置
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "data/zhichang_zuiti.db")


config = Config()
