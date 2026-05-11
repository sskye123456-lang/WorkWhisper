# Card Builder
from app.models.user import PersonaType, PERSONAS, ReplySuggestion
from app.quiz.questions import QuizQuestion
from app.config import config


class CardBuilder:
    @staticmethod
    def welcome_card() -> dict:
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "职场嘴替"}, "template": "blue"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "打工人的嘴替来了！把同事的消息发给我，我帮你用不同风格回复。"}},
                {"tag": "div", "text": {"tag": "lark_md", "content": "发送任意消息即可开始，或输入 **帮助** 查看指令。"}},
            ]
        }

    @staticmethod
    def quiz_card(question: QuizQuestion, progress: int) -> dict:
        elements = []
        for i, opt in enumerate(question.options):
            label = chr(65 + i) + ". " + opt["text"][:30]
            elements.append({
                "tag": "button",
                "text": {"content": label, "tag": "plain_text"},
                "value": {"action": "answer", "question_id": question.id, "answer": chr(65 + i)},
                "type": "default",
            })
        total = 5
        progress_text = "第 " + str(progress + 1) + " / " + str(total) + " 题"
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "职场人格测试 - " + progress_text}, "template": "turquoise"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "**" + question.question + "**"}},
                {"tag": "action", "actions": elements}
            ]
        }

    @staticmethod
    def quiz_result_card(persona: PersonaType, scores: dict) -> dict:
        p = PERSONAS[persona]
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "你的职场人格是 " + p.emoji + " " + p.title},
                "template": p.header_template
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "> " + p.quote}},
                {"tag": "div", "text": {"tag": "lark_md", "content": p.description}},
                {"tag": "action", "actions": [
                    {"tag": "button", "text": {"content": "开始使用", "tag": "plain_text"},
                     "value": {"action": "confirm_persona", "persona": persona.value}, "type": "primary"}
                ]}
            ]
        }

    @staticmethod
    def persona_select_card(current_persona: PersonaType = None) -> dict:
        elements = []
        for p_type, p in PERSONAS.items():
            btn_type = "primary" if p_type == current_persona else "default"
            elements.append({
                "tag": "button",
                "text": {"content": p.emoji + " " + p.title, "tag": "plain_text"},
                "value": {"action": "select_persona", "persona": p_type.value},
                "type": btn_type,
            })
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "选择你的职场人设"}},
            "elements": [{"tag": "action", "actions": elements}]
        }

    @staticmethod
    def reply_card(suggestion: ReplySuggestion, original_message: str, remaining: int = 3) -> dict:
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "回复建议"}, "template": "blue"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "**对方说：**\n" + original_message}},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**温和版：**\n" + suggestion.mild}},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**标准版：**\n" + suggestion.standard}},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**火力版：**\n" + suggestion.fire}},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "剩余外援次数：" + str(remaining) + " | 输入「请外援」呼叫其他风格"}]}
            ]
        }

    @staticmethod
    def reinforcement_select_card(current_persona: PersonaType, remaining: int) -> dict:
        elements = []
        for p_type, p in PERSONAS.items():
            if p_type != current_persona:
                elements.append({
                    "tag": "button",
                    "text": {"content": p.emoji + " " + p.title, "tag": "plain_text"},
                    "value": {"action": "call_reinforcement", "persona": p_type.value},
                    "type": "default",
                })
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "请外援（剩余 " + str(remaining) + " 次）"}},
            "elements": [{"tag": "action", "actions": elements}] if elements else [{"tag": "div", "text": {"tag": "plain_text", "content": "没有其他可用的人设"}}]
        }

    @staticmethod
    def reinforcement_exhaust_card() -> dict:
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "外援次数已用完"}, "template": "red"},
            "elements": [{"tag": "div", "text": {"tag": "plain_text", "content": "今天的外援次数已经用完了，明天再来吧！"}}]
        }

    @staticmethod
    def help_card() -> dict:
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "职场嘴替 - 使用帮助"}, "template": "blue"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "**使用方法：**\n1. 把同事的消息发给我\n2. 我会生成 3 种风格的回复\n3. 选一个你喜欢的复制发送！"}},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**指令列表：**\n- 帮助 / help - 显示帮助\n- 换人设 / switch - 切换人设\n- 请外援 - 呼叫其他风格\n- 重新测试 - 重做人格测试"}},
            ]
        }

    @staticmethod
    def simple_text_card(text: str, template: str = "blue") -> dict:
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": text[:100]}, "template": template},
            "elements": []
        }


card_builder = CardBuilder()
