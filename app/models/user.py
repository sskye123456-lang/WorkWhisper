# Data Models
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
from datetime import datetime


class PersonaType(str, Enum):
    SHA_SENG = "sha_seng"
    HANZAWA_NAOKI = "hanzawa_naoki"
    ZHEN_HUAN = "zhen_huan"
    YU_HUA = "yu_hua"
    YUE_YUNPENG = "yue_yunpeng"
    XIAO_S = "xiao_s"


class UserState(str, Enum):
    NEW = "new"
    IN_QUIZ = "in_quiz"
    HAS_PERSONA = "has_persona"


@dataclass
class Persona:
    id: PersonaType
    name: str
    emoji: str
    title: str
    quote: str
    description: str
    color: str
    header_template: str


PERSONAS: Dict[PersonaType, Persona] = {
    PersonaType.SHA_SENG: Persona(
        id=PersonaType.SHA_SENG, name="sha_seng", emoji="\U0001f54a\ufe0f",
        title="\u548c\u4e8b\u4f6c\u00b7\u6c99\u50e7",
        quote="\u5927\u5e08\u5144\u8bf4\u5f97\u5bf9",
        description="\u9644\u548c\u5373\u5b89\u5168\uff0c\u8c01\u4e5f\u4e0d\u5f97\u7f6a",
        color="#FFE4E1", header_template="pink"
    ),
    PersonaType.HANZAWA_NAOKI: Persona(
        id=PersonaType.HANZAWA_NAOKI, name="hanzawa", emoji="\U0001f525",
        title="\u6574\u987f\u4fa0\u00b7\u534a\u6cfd\u76f4\u6811",
        quote="\u4ee5\u7259\u8fd8\u7259\uff0c\u52a0\u500d\u5949\u8fd8",
        description="\u76f4\u7403\u62d2\u7edd\uff0c\u7528\u89c4\u5219\u5bf9\u6297PUA",
        color="#FF6B35", header_template="orange"
    ),
    PersonaType.ZHEN_HUAN: Persona(
        id=PersonaType.ZHEN_HUAN, name="zhen_huan", emoji="\U0001f300",
        title="\u592a\u6781\u738b\u00b7\u7504\u5b1b",
        quote="\u8bdd\u4e0d\u8bf4\u6ee1\uff0c\u4e8b\u4e0d\u505a\u7edd",
        description="\u6ef4\u6c34\u4e0d\u6f0f\uff0c\u628a\u7403\u8e22\u56de\u53bb",
        color="#6B5B95", header_template="violet"
    ),
    PersonaType.YU_HUA: Persona(
        id=PersonaType.YU_HUA, name="yu_hua", emoji="\U0001f9ca",
        title="\u901a\u900f\u6d3e\u00b7\u4f59\u534e",
        quote="\u6d3b\u7740\u672c\u8eab\u5c31\u662f\u610f\u4e49",
        description="\u5e7d\u9ed8\u5316\u89e3\u5c34\u5c2c\uff0c\u8c41\u8fbe\u9762\u5bf9\u4e00\u5207",
        color="#4A4A4A", header_template="grey"
    ),
    PersonaType.YUE_YUNPENG: Persona(
        id=PersonaType.YUE_YUNPENG, name="yue_yunpeng", emoji="\U0001f3ad",
        title="\u6367\u54c5\u738b\u00b7\u5cb3\u4e91\u9e4f",
        quote="\u54ce\u5466\u5582\uff0c\u60a8\u8bf4\u5f97\u5bf9\uff01",
        description="\u7b11\u7740\u7cca\u5f04\uff0c\u81ea\u5632\u5373\u94e0\u7532",
        color="#FAAD14", header_template="yellow"
    ),
    PersonaType.XIAO_S: Persona(
        id=PersonaType.XIAO_S, name="xiao_s", emoji="\U0001f480",
        title="\u6bd2\u820c\u541b\u00b7\u5c0fS",
        quote="\u4f60\u5728\u8bf4\u4ec0\u4e48\u9b3c\u554a\uff1f",
        description="\u72b9\u5229\u5410\u69fd\uff0c\u4e00\u9488\u89c1\u8840",
        color="#F5222D", header_template="red"
    ),
}


@dataclass
class User:
    open_id: str
    state: UserState = UserState.NEW
    current_persona: Optional[PersonaType] = None
    quiz_progress: int = 0
    quiz_answers: List[str] = field(default_factory=list)
    reinforcement_count: int = 0
    reinforcement_reset_date: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def get_reinforcement_remaining(self, daily_limit: int) -> int:
        today = datetime.now().strftime("%Y-%m-%d")
        if self.reinforcement_reset_date != today:
            self.reinforcement_count = 0
            self.reinforcement_reset_date = today
        return max(0, daily_limit - self.reinforcement_count)


@dataclass
class QuizQuestion:
    id: int
    scene: str
    question: str
    options: List[Dict[str, str]]
    is_ghost: bool = False


@dataclass
class ReplySuggestion:
    mild: str
    standard: str
    fire: str
    persona: PersonaType
    original_message: str
