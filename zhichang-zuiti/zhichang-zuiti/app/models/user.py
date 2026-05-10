"""
职场嘴替 - 数据模型
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
from datetime import datetime


class PersonaType(str, Enum):
    """人设类型"""
    SHA_SENG = "sha_seng"  # 和事佬·沙僧
    HANZAWA_NAOKI = "hanzawa_naoki"  # 整顿侠·半泽直树
    ZHEN_HUAN = "zhen_huan"  # 太极王·甄嬛
    YU_HUA = "yu_hua"  # 通透派·余华
    YUE_YUNPENG = "yue_yunpeng"  # 捧哏王·岳云鹏
    XIAO_S = "xiao_s"  # 毒舌君·小S


class ReplyVersion(str, Enum):
    """回复版本"""
    MILD = "mild"  # 温和版
    STANDARD = "standard"  # 标准版
    FIRE = "fire"  # 火力版


class UserState(str, Enum):
    """用户状态"""
    NEW = "new"  # 新用户，未选人设
    IN_QUIZ = "in_quiz"  # 正在做测试
    HAS_PERSONA = "has_persona"  # 已选人设
    WAITING_REPLY = "waiting_reply"  # 等待回复生成


@dataclass
class Persona:
    """人设信息"""
    id: PersonaType
    name: str
    emoji: str
    title: str
    quote: str
    description: str
    color: str
    header_template: str


# 六大人设定义
PERSONAS: Dict[PersonaType, Persona] = {
    PersonaType.SHA_SENG: Persona(
        id=PersonaType.SHA_SENG,
        name="沙僧",
        emoji="🕊️",
        title="和事佬·沙僧",
        quote="大师兄说得对",
        description="附和即安全，谁也不得罪",
        color="#FFE4E1",
        header_template="pink"
    ),
    PersonaType.HANZAWA_NAOKI: Persona(
        id=PersonaType.HANZAWA_NAOKI,
        name="半泽直树",
        emoji="🔥",
        title="整顿侠·半泽直树",
        quote="以牙还牙，加倍奉还",
        description="直球拒绝，用规则对抗PUA",
        color="#FF6B35",
        header_template="orange"
    ),
    PersonaType.ZHEN_HUAN: Persona(
        id=PersonaType.ZHEN_HUAN,
        name="甄嬛",
        emoji="🌀",
        title="太极王·甄嬛",
        quote="话不说满，事不做绝",
        description="滴水不漏，把球踢回去",
        color="#6B5B95",
        header_template="violet"
    ),
    PersonaType.YU_HUA: Persona(
        id=PersonaType.YU_HUA,
        name="余华",
        emoji="🧊",
        title="通透派·余华",
        quote="活着本身就是意义",
        description="幽默化解尴尬，豁达面对一切",
        color="#4A4A4A",
        header_template="grey"
    ),
    PersonaType.YUE_YUNPENG: Persona(
        id=PersonaType.YUE_YUNPENG,
        name="岳云鹏",
        emoji="🎭",
        title="捧哏王·岳云鹏",
        quote="哎哟喂，您说得对！",
        description="笑着糊弄，自嘲即铠甲",
        color="#FAAD14",
        header_template="yellow"
    ),
    PersonaType.XIAO_S: Persona(
        id=PersonaType.XIAO_S,
        name="小S",
        emoji="💀",
        title="毒舌君·小S",
        quote="你在说什么鬼啊？",
        description="犀利吐槽，一针见血",
        color="#F5222D",
        header_template="red"
    ),
}


@dataclass
class User:
    """用户数据"""
    open_id: str  # 飞书用户ID
    state: UserState = UserState.NEW
    current_persona: Optional[PersonaType] = None
    quiz_progress: int = 0  # 测试进度 (0-22)
    quiz_answers: List[str] = field(default_factory=list)  # 测试答案
    reinforcement_count: int = 0  # 今日请外援次数
    reinforcement_reset_date: str = ""  # 请外援次数重置日期
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def get_persona_scores(self) -> Dict[PersonaType, int]:
        """计算人设得分"""
        scores = {p: 0 for p in PersonaType}
        # TODO: 根据quiz_answers计算得分
        return scores

    def get_reinforcement_remaining(self, daily_limit: int) -> int:
        """获取剩余请外援次数"""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.reinforcement_reset_date != today:
            self.reinforcement_count = 0
            self.reinforcement_reset_date = today
        return max(0, daily_limit - self.reinforcement_count)


@dataclass
class QuizQuestion:
    """测试题"""
    id: int
    scene: str  # 场景描述
    question: str  # 问题
    options: List[Dict[str, str]]  # 选项列表 [{"text": "...", "persona": "sha_seng"}, ...]
    is_ghost: bool = False  # 是否是鬼畜题
    ghost_theme: Optional[str] = None  # 鬼畜题主题


@dataclass
class ReplySuggestion:
    """回复建议"""
    mild: str  # 温和版
    standard: str  # 标准版
    fire: str  # 火力版
    persona: PersonaType
    original_message: str
