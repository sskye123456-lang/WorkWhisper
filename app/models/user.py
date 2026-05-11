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
        id=PersonaType.SHA_SENG, name="sha_seng", emoji="🕊️",
        title="和事佬·沙僧",
        quote="大师兄说得对",
        description="附和即安全，谁也不得罪",
        color="#FFE4E1", header_template="pink"
    ),
    PersonaType.HANZAWA_NAOKI: Persona(
        id=PersonaType.HANZAWA_NAOKI, name="hanzawa", emoji="🔥",
        title="整顿侠·半泽直树",
        quote="以牙还牙，加倍奉还",
        description="直球拒绝，用规则对抗PUA",
        color="#FF6B35", header_template="orange"
    ),
    PersonaType.ZHEN_HUAN: Persona(
        id=PersonaType.ZHEN_HUAN, name="zhen_huan", emoji="🌀",
        title="太极王·甄嬛",
        quote="话不说满，事不做绝",
        description="滴水不漏，把球踢回去",
        color="#6B5B95", header_template="violet"
    ),
    PersonaType.YU_HUA: Persona(
        id=PersonaType.YU_HUA, name="yu_hua", emoji="🧊",
        title="通透派·余华",
        quote="活着本身就是意义",
        description="幽默化解尴尬，豁达面对一切",
        color="#4A4A4A", header_template="grey"
    ),
    PersonaType.YUE_YUNPENG: Persona(
        id=PersonaType.YUE_YUNPENG, name="yue_yunpeng", emoji="🎭",
        title="捧哏王·岳云鹏",
        quote="哎呦喂，您说得对！",
        description="笑着糊弄，自嘲即铠甲",
        color="#FAAD14", header_template="yellow"
    ),
    PersonaType.XIAO_S: Persona(
        id=PersonaType.XIAO_S, name="xiao_s", emoji="💀",
        title="毒舌君·小S",
        quote="你在说什么鬼啊？",
        description="犀利吐槽，一针见血",
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
