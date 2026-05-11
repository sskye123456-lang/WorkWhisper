# Card Builder
from app.models.user import PersonaType, PERSONAS, ReplySuggestion
from app.quiz.questions import QuizQuestion
from app.config import config


class CardBuilder:
    @staticmethod
    def welcome_card() -> dict:
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "职场嘴替 - 打工人的嘴替"}, "template": "blue"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "**\ud83d\udc4b \u6b22\u8fce\u4f7f\u7528\u804c\u573a\u5634\u66ff\uff01**\n\n\u628a\u540c\u4e8b\u7684\u6d88\u606f\u53d1\u7ed9\u6211\uff0c\u6211\u7528\u4f60\u7684\u4eba\u8bbe\u98ce\u683c\u5e2e\u4f60\u56de\u590d\uff0c\u5305\u62ec **\u6e29\u548c\u7248 / \u6807\u51c6\u7248 / \u706b\u529b\u7248** \u4e09\u79cd\u98ce\u683c\u3002"}},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**\ud83c\udfaf \u5148\u505a\u4e2a\u6d4b\u8bd5\uff0c\u627e\u51fa\u4f60\u7684\u804c\u573a\u4eba\u683c**\n\n\u6d4b\u8bd5\u5c06\u6839\u636e\u4f60\u7684\u9009\u62e9\uff0c\u5212\u5206\u4e3a **\u548c\u4e8b\u4f6c\u3001\u6574\u987f\u4fa0\u3001\u592a\u6781\u738b\u3001\u901a\u900f\u6d3e\u3001\u6367\u54c5\u738b\u3001\u6bd2\u820c\u541b** \u516d\u79cd\u4eba\u8bbe\uff0c\u7136\u540e\u6211\u5c31\u7528\u8fd9\u4e2a\u98ce\u683c\u5e2e\u4f60\u56de\u590d\u4e86\u3002"}},
                {"tag": "action", "actions": [
                    {"tag": "button", "text": {"content": "\ud83c\udf89 \u5f00\u59cb\u6d4b\u8bd5", "tag": "plain_text"}, "value": {"action": "start_quiz"}, "type": "primary"},
                    {"tag": "button", "text": {"content": "\ud83d\udcf1 \u5148\u770b\u770b\u7528\u6cd5", "tag": "plain_text"}, "value": {"action": "help"}, "type": "default"},
                ]},
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
        total = 20
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
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**\ud83d\ude80 想不想逆袭体验另一种职场人生？**\n选择一种人格作为你的嘴替风格，以后都会默认用这个风格帮你回复哦～"}},
                {"tag": "action", "actions": [
                    {"tag": "button", "text": {"content": "\u2728 就用 " + p.title + " 了", "tag": "plain_text"},
                     "value": {"action": "confirm_persona", "persona": persona.value}, "type": "primary"},
                    {"tag": "button", "text": {"content": "\ud83d\ude80 逆袭！换一种人格", "tag": "plain_text"},
                     "value": {"action": "want_counterattack"}, "type": "default"},
                ]}
            ]
        }

    @staticmethod
    def counterattack_select_card(original_persona: PersonaType) -> dict:
        """逆袭体验选择卡片 - 让用户选一种人格作为默认嘴替"""
        op = PERSONAS[original_persona]
        elements = []
        for p_type, p in PERSONAS.items():
            btn_type = "primary" if p_type == original_persona else "default"
            label = p.emoji + " " + p.title
            if p_type == original_persona:
                label += "（测试结果）"
            elements.append({
                "tag": "button",
                "text": {"content": label, "tag": "plain_text"},
                "value": {"action": "counterattack_select", "persona": p_type.value},
                "type": btn_type,
            })
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "\ud83d\ude80 逆袭体验 - 选择你的职场嘴替"}},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md",
                    "content": "你的测试结果是 **" + op.emoji + " " + op.title + "**\n\n但人生苦短，想换个活法吗？\n选择一种人格作为你的**默认嘴替风格**，以后所有回复都会用这个风格～\n\n随时发送「换人设」可以重新选择。"}},
                {"tag": "action", "actions": elements}
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
