"""
职场嘴替 - 飞书消息卡片生成
"""
import json
from typing import Optional, Dict, List
from app.models.user import PersonaType, PERSONAS, ReplySuggestion, User
from app.quiz.questions import QuizQuestion, QUIZ_QUESTIONS
from app.config import config


class CardBuilder:
    """飞书消息卡片构建器"""
    
    @staticmethod
    def welcome_card(has_persona: bool = False, current_persona: PersonaType = None) -> dict:
        """欢迎语卡片"""
        if has_persona and current_persona:
            persona = PERSONAS[current_persona]
            return {
                "schema": "2.0",
                "header": {
                    "title": {"tag": "plain_text", "content": "👋 欢迎回来！"},
                    "template": persona.header_template
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": f"当前人设：{persona.emoji} {persona.title}\n\"{persona.quote}\""
                    },
                    {"tag": "hr"},
                    {
                        "tag": "markdown",
                        "content": "💬 把同事的消息发给我，我帮你回复\n\n支持输入方式：\n📝 直接打字 / 📷 截图识别 / 📨 转发对话"
                    },
                    {"tag": "hr"},
                    {
                        "tag": "action",
                        "actions": [
                            {"tag": "button", "text": {"tag": "plain_text", "content": "🔄 换人设"}, "type": "default", "value": {"action": "switch_persona"}},
                            {"tag": "button", "text": {"tag": "plain_text", "content": "🆘 请外援"}, "type": "primary_text", "value": {"action": "call_reinforcement"}},
                            {"tag": "button", "text": {"tag": "plain_text", "content": "📖 帮助"}, "type": "default", "value": {"action": "help"}},
                        ]
                    },
                ]
            }
        
        return {
            "schema": "2.0",
            "header": {
                "title": {"tag": "plain_text", "content": "👋 你好！我是【职场嘴替】"},
                "template": "turquoise"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": "还在为不知道怎么回同事消息而发愁？\n让我来替你**\"说话\"**！"
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": "**🧪 先做个测试，看看你是哪种职场人？**\n22道题，4-5分钟，测出你的职场嘴替"
                },
                {
                    "tag": "markdown",
                    "content": "六种风格等你解锁：\n🕊️ 和事佬·沙僧 — \"大师兄说得对\"\n🔥 整顿侠·半泽直树 — \"以牙还牙，加倍奉还\"\n🌀 太极王·甄嬛 — \"话不说满，事不做绝\"\n🧊 通透派·余华 — \"活着本身就是意义\"\n🎭 捧哏王·岳云鹏 — \"哎哟喂，您说得对！\"\n💀 毒舌君·小S — \"你在说什么鬼啊？\""
                },
                {"tag": "hr"},
                {
                    "tag": "action",
                    "actions": [
                        {"tag": "button", "text": {"tag": "plain_text", "content": "🧪 开始测试"}, "type": "primary", "value": {"action": "start_quiz"}},
                        {"tag": "button", "text": {"tag": "plain_text", "content": "⚡ 直接选人设"}, "type": "default", "value": {"action": "select_persona"}},
                    ]
                },
            ]
        }
    
    @staticmethod
    def quiz_card(question: QuizQuestion, progress: int) -> dict:
        """测试题卡片"""
        total = len(QUIZ_QUESTIONS)
        percentage = int(progress / total * 100)
        
        header_title = f"🧪 第{question.id}题 / 共{total}题"
        header_template = "turquoise"
        
        if question.is_ghost:
            header_title = f"🤪 鬼畜时间！第{question.id}题 / 共{total}题"
            ghost_templates = {
                "便秘": "orange",
                "外卖迟到": "yellow",
                "地铁被踩": "red",
                "理发翻车": "purple",
                "手机没电": "blue",
                "荒岛选择": "green",
            }
            header_template = ghost_templates.get(question.ghost_theme, "orange")
        
        elements = [
            {
                "tag": "markdown",
                "content": f"{'█' * (percentage // 5)}{'░' * (20 - percentage // 5)} **{percentage}%**"
            },
            {"tag": "hr"},
            {
                "tag": "markdown",
                "content": f"{question.scene}\n\n{question.question}"
            },
        ]
        
        # 添加选项按钮
        for i, option in enumerate(question.options):
            option_label = chr(65 + i)  # A, B, C, D, E, F
            elements.append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": f"{option_label}. {option['text'][:50]}..."},
                        "type": "default",
                        "width": "fill",
                        "value": {
                            "action": "answer",
                            "question_id": question.id,
                            "answer": option_label,
                        }
                    }
                ]
            })
        
        return {
            "schema": "2.0",
            "header": {
                "title": {"tag": "plain_text", "content": header_title},
                "template": header_template
            },
            "elements": elements
        }
    
    @staticmethod
    def quiz_result_card(persona: PersonaType, scores: dict) -> dict:
        """测试结果卡片"""
        p = PERSONAS[persona]
        
        # 构建成分分析
        score_lines = []
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for p_type, score in sorted_scores:
            p_info = PERSONAS[p_type]
            bar_len = int(score / 22 * 10)
            score_lines.append(f"{p_info.emoji} {p_info.name.split('·')[0]}  {'█' * bar_len}{'░' * (10 - bar_len)} {int(score / 22 * 100)}%")
        
        return {
            "schema": "2.0",
            "header": {
                "title": {"tag": "plain_text", "content": "🎯 测试完成！"},
                "template": p.header_template
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": f"你的职场嘴替是：\n\n**{p.emoji} {p.title}**\n\n\"{p.quote}\""
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": "📊 人设成分分析：\n" + "\n".join(score_lines)
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": "🤔 这是你现在的状态，但不一定是你的终点\n\n想不想体验一下另一种人生？"
                },
                {
                    "tag": "action",
                    "actions": [
                        {"tag": "button", "text": {"tag": "plain_text", "content": f"保持{p.name}"}, "type": "primary", "value": {"action": "confirm_persona", "persona": persona.value}},
                        {"tag": "button", "text": {"tag": "plain_text", "content": "试试其他人设"}, "type": "default", "value": {"action": "select_persona"}},
                    ]
                },
            ]
        }
    
    @staticmethod
    def persona_select_card(current_persona: PersonaType = None) -> dict:
        """人设选择卡片"""
        elements = [
            {
                "tag": "markdown",
                "content": "选择你的职场嘴替："
            },
            {"tag": "hr"},
        ]
        
        for p_type, p in PERSONAS.items():
            is_current = p_type == current_persona
            elements.append({
                "tag": "markdown",
                "content": f"**{p.emoji} {p.title}**\n\"{p.quote}\" · {p.description}"
            })
            elements.append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "当前人设" if is_current else "选择"},
                        "type": "primary" if is_current else "default",
                        "disabled": is_current,
                        "value": {"action": "select_persona", "persona": p_type.value}
                    }
                ]
            })
        
        return {
            "schema": "2.0",
            "header": {
                "title": {"tag": "plain_text", "content": "⚡ 选择人设"},
                "template": "blue"
            },
            "elements": elements
        }
    
    @staticmethod
    def reply_card(
        suggestion: ReplySuggestion, 
        original_message: str,
        reinforcement_remaining: int = 3
    ) -> dict:
        """回复建议卡片"""
        persona = PERSONAS[suggestion.persona]
        
        return {
            "schema": "2.0",
            "header": {
                "title": {"tag": "plain_text", "content": "📩 收到同事消息"},
                "template": persona.header_template
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": f"**原始消息：**\n> {original_message}"
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": f"{persona.emoji} 用【{persona.title}】人设回复："
                },
                # 温和版
                {
                    "tag": "markdown",
                    "content": f"**🟢 温和版**\n> {suggestion.mild}"
                },
                {
                    "tag": "action",
                    "actions": [
                        {"tag": "button", "text": {"tag": "plain_text", "content": "📋 复制"}, "type": "default", "size": "small", "value": {"action": "copy", "text": suggestion.mild}}
                    ]
                },
                {"tag": "hr"},
                # 标准版
                {
                    "tag": "markdown",
                    "content": f"**🟡 标准版**\n> {suggestion.standard}"
                },
                {
                    "tag": "action",
                    "actions": [
                        {"tag": "button", "text": {"tag": "plain_text", "content": "📋 复制"}, "type": "default", "size": "small", "value": {"action": "copy", "text": suggestion.standard}}
                    ]
                },
                {"tag": "hr"},
                # 火力版
                {
                    "tag": "markdown",
                    "content": f"**🔴 火力版**\n> {suggestion.fire}"
                },
                {
                    "tag": "action",
                    "actions": [
                        {"tag": "button", "text": {"tag": "plain_text", "content": "📋 复制"}, "type": "default", "size": "small", "value": {"action": "copy", "text": suggestion.fire}}
                    ]
                },
                {"tag": "hr"},
                # 操作按钮
                {
                    "tag": "action",
                    "actions": [
                        {"tag": "button", "text": {"tag": "plain_text", "content": "🆘 请外援"}, "type": "primary_text", "value": {"action": "call_reinforcement"}},
                        {"tag": "button", "text": {"tag": "plain_text", "content": "🔄 换人设"}, "type": "default", "value": {"action": "switch_persona"}},
                    ]
                },
                {
                    "tag": "markdown",
                    "content": f"🆘 今日请外援剩余：{reinforcement_remaining}/{config.REINFORCEMENT_DAILY_LIMIT}"
                },
            ]
        }
    
    @staticmethod
    def reinforcement_select_card(current_persona: PersonaType, remaining: int) -> dict:
        """请外援选择卡片"""
        elements = [
            {
                "tag": "markdown",
                "content": f"当前人设：{PERSONAS[current_persona].emoji} {PERSONAS[current_persona].title}\n选择一个外援人设来帮你回复："
            },
            {"tag": "hr"},
        ]
        
        for p_type, p in PERSONAS.items():
            if p_type == current_persona:
                continue
            elements.append({
                "tag": "markdown",
                "content": f"**{p.emoji} {p.title}**\n\"{p.quote}\""
            })
            elements.append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": f"呼叫{p.name}"},
                        "type": "default",
                        "value": {"action": "call_reinforcement", "persona": p_type.value}
                    }
                ]
            })
        
        elements.append({"tag": "hr"})
        elements.append({
            "tag": "markdown",
            "content": f"🆘 今日请外援剩余：**{remaining}/{config.REINFORCEMENT_DAILY_LIMIT}**（每日0点重置）"
        })
        
        return {
            "schema": "2.0",
            "header": {
                "title": {"tag": "plain_text", "content": "🆘 请外援 — 呼叫其他职场嘴替"},
                "template": "purple"
            },
            "elements": elements
        }
    
    @staticmethod
    def reinforcement_exhaust_card() -> dict:
        """请外援次数用完卡片"""
        return {
            "schema": "2.0",
            "header": {
                "title": {"tag": "plain_text", "content": "🆘 今日请外援次数已用完"},
                "template": "red"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": f"你今天已经用了{config.REINFORCEMENT_DAILY_LIMIT}次请外援，明天0点重置。"
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": "💡 你可以：\n• 继续使用当前人设回复\n• 切换人设（切换后永久生效，不消耗请外援次数）\n• 升级Pro，解锁无限次请外援"
                },
                {
                    "tag": "action",
                    "actions": [
                        {"tag": "button", "text": {"tag": "plain_text", "content": "🔄 换人设"}, "type": "default", "value": {"action": "switch_persona"}},
                        {"tag": "button", "text": {"tag": "plain_text", "content": "💎 了解Pro"}, "type": "primary", "value": {"action": "upgrade_pro"}},
                    ]
                },
            ]
        }
    
    @staticmethod
    def help_card() -> dict:
        """帮助卡片"""
        return {
            "schema": "2.0",
            "header": {
                "title": {"tag": "plain_text", "content": "📖 使用说明"},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": """**1️⃣ 选择人设**

先做测试或直接从6个人设中选择一个：
🕊️ 和事佬·沙僧 — 委婉附和，不得罪人
🔥 整顿侠·半泽直树 — 直球拒绝，守住边界
🌀 太极王·甄嬛 — 滴水不漏，把球踢走
🧊 通透派·余华 — 幽默豁达，不内耗
🎭 捧哏王·岳云鹏 — 笑着糊弄，自嘲化解
💀 毒舌君·小S — 犀利吐槽，一针见血"""
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": """**2️⃣ 发送同事消息**

三种输入方式：
📝 直接打字或粘贴同事消息
📷 截图对话（自动OCR识别文字）
📨 飞书内转发对话"""
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": """**3️⃣ 获取回复建议**

每次生成3个版本的回复：
🟢 温和版 — 最柔和，适合敏感关系
🟡 标准版 — 平衡型，日常使用
🔴 火力版 — 最强硬，适合对方越界时"""
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": """**4️⃣ 请外援**

当前人设搞不定？呼叫其他人设来帮忙！
免费用户每日3次，Pro用户无限次"""
                },
                {"tag": "hr"},
                {
                    "tag": "markdown",
                    "content": """**快捷指令：**
• "换人设" — 切换到其他人设
• "请外援" — 呼叫其他人设回复
• "重新测试" — 再做一次人格测试
• "帮助" — 查看本说明"""
                },
            ]
        }
    
    @staticmethod
    def simple_text_card(text: str, template: str = "blue") -> dict:
        """简单文本卡片"""
        return {
            "schema": "2.0",
            "header": {
                "title": {"tag": "plain_text", "content": "💬"},
                "template": template
            },
            "elements": [
                {"tag": "markdown", "content": text}
            ]
        }


# 全局卡片构建器
card_builder = CardBuilder()
