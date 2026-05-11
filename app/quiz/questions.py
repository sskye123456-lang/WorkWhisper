# Quiz Questions
from app.models.user import QuizQuestion, PersonaType

QUIZ_QUESTIONS = [
    QuizQuestion(
        id=1, scene="meeting",
        question="会议上老板问：大家有什么问题吗？",
        options=[
            {"text": "没有问题，都很好", "persona": "sha_seng"},
            {"text": "我有些想说", "persona": "hanzawa_naoki"},
            {"text": "我先想想再回复", "persona": "zhen_huan"},
            {"text": "哈哈有趣，这会开得不错", "persona": "yue_yunpeng"},
            {"text": "问了也白问，没人听", "persona": "xiao_s"},
            {"text": "人生就是这样，下班吧", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=2, scene="deadline",
        question="同事说：这个今天能完成吗？",
        options=[
            {"text": "好的好的，没问题！", "persona": "sha_seng"},
            {"text": "这个进度不太合理吧", "persona": "hanzawa_naoki"},
            {"text": "我看看日程安排", "persona": "zhen_huan"},
            {"text": "哎呦喂，你要命啊！", "persona": "yue_yunpeng"},
            {"text": "你认真的吗？", "persona": "xiao_s"},
            {"text": "元气消耗完就好，不用急", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=3, scene="feedback",
        question="老板当众批评了你的工作",
        options=[
            {"text": "谢谢老板指导！", "persona": "sha_seng"},
            {"text": "我不完全同意这个评价", "persona": "hanzawa_naoki"},
            {"text": "感谢您的反馈，我会改进", "persona": "zhen_huan"},
            {"text": "哈哈，被批了啊，我心里有数", "persona": "yue_yunpeng"},
            {"text": "啦？请问我哪里做得不好？", "persona": "xiao_s"},
            {"text": "痛苦是人生的常态", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=4, scene="overtime",
        question="周末被要求加班",
        options=[
            {"text": "好的，我来加班", "persona": "sha_seng"},
            {"text": "周末加班违反劳动法", "persona": "hanzawa_naoki"},
            {"text": "我看看能不能协调一下", "persona": "zhen_huan"},
            {"text": "我的周末！不行啊！", "persona": "yue_yunpeng"},
            {"text": "你在开玩笑吗？", "persona": "xiao_s"},
            {"text": "加班也是一种休息，反正回家也无聊", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=5, scene="credit",
        question="同事抢了你的功劳",
        options=[
            {"text": "没事，团队成果最重要", "persona": "sha_seng"},
            {"text": "这其实是我做的", "persona": "hanzawa_naoki"},
            {"text": "很高兴项目成功了", "persona": "zhen_huan"},
            {"text": "哎，你真牛！下次带带我！", "persona": "yue_yunpeng"},
            {"text": "我想我耳朵出问题了", "persona": "xiao_s"},
            {"text": "世界上没有什么是真正属于我们的", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=6, scene="lunch",
        question="同事问你中午吃什么，然后说他们要点外卖，问你吃什么",
        options=[
            {"text": "我都行，跟你们一起吃", "persona": "sha_seng"},
            {"text": "我已经带饭了，不用了谢谢", "persona": "hanzawa_naoki"},
            {"text": "我再看看吧，等会回复你", "persona": "zhen_huan"},
            {"text": "点外卖？那我可太开心了！", "persona": "yue_yunpeng"},
            {"text": "你们每次都这样，我已经不想说了", "persona": "xiao_s"},
            {"text": "吃什么不重要，能吃饱就行", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=7, scene="chat",
        question="群里有人发了一个很冷的笑话，全场寂静",
        options=[
            {"text": "哈哈，还行还行，我笑了", "persona": "sha_seng"},
            {"text": "这个时候就不要说话了吧", "persona": "hanzawa_naoki"},
            {"text": "哈哈，你很有意思啊", "persona": "zhen_huan"},
            {"text": "我来换个！听我说……", "persona": "yue_yunpeng"},
            {"text": "屏幕都尴尬了，我为你尴尬", "persona": "xiao_s"},
            {"text": "尴尬是社交的常态，不用在意", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=8, scene="leave",
        question="你想请假，但老板说现在很忙",
        options=[
            {"text": "好的，那我再等等", "persona": "sha_seng"},
            {"text": "我已经提前安排好工作了", "persona": "hanzawa_naoki"},
            {"text": "理解，那我看看其他时间", "persona": "zhen_huan"},
            {"text": "忙到这种程度，老板也不容易啊", "persona": "yue_yunpeng"},
            {"text": "每次都忙，我是机器人吗？", "persona": "xiao_s"},
            {"text": "人生苦短，该休息就休息吧", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=9, scene="group",
        question="同事在群里 @你，让你帮忙做一个不属于你的任务",
        options=[
            {"text": "好的，我来看看", "persona": "sha_seng"},
            {"text": "这不是我的工作范围", "persona": "hanzawa_naoki"},
            {"text": "我手头有点事，你先找别人吧", "persona": "zhen_huan"},
            {"text": "哎呦喂，你这是看上我了啊！", "persona": "yue_yunpeng"},
            {"text": "你 @我就是让我干活？", "persona": "xiao_s"},
            {"text": "帮人家就是帮自己，不急", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=10, scene="promotion",
        question="同事被提拔了，但你觉得他能力不如你",
        options=[
            {"text": "恭喜你啊，以后多关照", "persona": "sha_seng"},
            {"text": "这个结果我无法接受", "persona": "hanzawa_naoki"},
            {"text": "公司的决定自然有它的道理", "persona": "zhen_huan"},
            {"text": "哈哈，那我以后就靠你照顾了！", "persona": "yue_yunpeng"},
            {"text": "笑死，这能力也提拔？", "persona": "xiao_s"},
            {"text": "世事难料，但没关系，过好自己的", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=11, scene="coffee",
        question="同事说请你喝咖啡，结果AA制",
        options=[
            {"text": "没事，大家都一样的", "persona": "sha_seng"},
            {"text": "你说请客结果AA？", "persona": "hanzawa_naoki"},
            {"text": "哦，那我下次请回来", "persona": "zhen_huan"},
            {"text": "哈哈，你这请客请得挺特别啊", "persona": "yue_yunpeng"},
            {"text": "你这是请客还是抢劫？", "persona": "xiao_s"},
            {"text": "咖啡的钱不重要，重要的是心情", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=12, scene="birthday",
        question="同事过生日，在群里发红包，你抢到了 0.01 元",
        options=[
            {"text": "谢谢！生日快乐！", "persona": "sha_seng"},
            {"text": "这个红包有点小吧", "persona": "hanzawa_naoki"},
            {"text": "运气不错，抢到就是赚到", "persona": "zhen_huan"},
            {"text": "哈哈，这个数字真吉利！", "persona": "yue_yunpeng"},
            {"text": "这么小气还发什么红包", "persona": "xiao_s"},
            {"text": "一分钱也是爱，比没有强", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=13, scene="wifi",
        question="公司WiFi很卡，老板说是大家流量用得太多",
        options=[
            {"text": "那我少用点手机", "persona": "sha_seng"},
            {"text": "这是基础设施问题，不是我们的错", "persona": "hanzawa_naoki"},
            {"text": "我看看能不能用自己的流量", "persona": "zhen_huan"},
            {"text": "哈哈，这是让我们好好工作的意思", "persona": "yue_yunpeng"},
            {"text": "你的WiFi是用来看的，不是用来用的？", "persona": "xiao_s"},
            {"text": "网络不好也是一种修行", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=14, scene="toilet",
        question="上厕所遇到老板，老板说你又来了",
        options=[
            {"text": "哈哈，最近肠胃不太好", "persona": "sha_seng"},
            {"text": "这是我的个人时间", "persona": "hanzawa_naoki"},
            {"text": "老板您也来了，真巧", "persona": "zhen_huan"},
            {"text": "哈哈，我们真是默契十足！", "persona": "yue_yunpeng"},
            {"text": "你管得有点多吧", "persona": "xiao_s"},
            {"text": "人生在世，有来有往，正常", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=15, scene="meeting_room",
        question="你预约的会议室被老板占用了",
        options=[
            {"text": "没事，我找别的地方", "persona": "sha_seng"},
            {"text": "这是我预约的，您应该提前说", "persona": "hanzawa_naoki"},
            {"text": "老板您先用，我等您", "persona": "zhen_huan"},
            {"text": "哈哈，老板您这是给我放假吗", "persona": "yue_yunpeng"},
            {"text": "预约系统是摆设吗？", "persona": "xiao_s"},
            {"text": "会议室不重要，重要的是心态", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=16, scene="rain",
        question="下雨天下班，同事开车顺路但没问你要不要搭车",
        options=[
            {"text": "没事，我打车回去", "persona": "sha_seng"},
            {"text": "你顺路不顺我吗？", "persona": "hanzawa_naoki"},
            {"text": "我看看公交怎么走", "persona": "zhen_huan"},
            {"text": "哈哈，你这车是两座的吧", "persona": "yue_yunpeng"},
            {"text": "我是透明人吗？", "persona": "xiao_s"},
            {"text": "淋雨也是一种体验", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=17, scene="printer",
        question="打印机卡纸了，同事说是你刚才用的那个人搞坏的",
        options=[
            {"text": "那我去看看能不能修", "persona": "sha_seng"},
            {"text": "刚才用的人很多，不能怪我", "persona": "hanzawa_naoki"},
            {"text": "可能是纸张问题，我换一包试试", "persona": "zhen_huan"},
            {"text": "哈哈，打印机也有脾气了", "persona": "yue_yunpeng"},
            {"text": "你看到是我搞的？", "persona": "xiao_s"},
            {"text": "打印机也需要休息，理解", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=18, scene="dress",
        question="老板说你穿得不够职业",
        options=[
            {"text": "好的，我明天换一套", "persona": "sha_seng"},
            {"text": "我的穿着并没有影响工作", "persona": "hanzawa_naoki"},
            {"text": "请问您对职业装有什么具体要求", "persona": "zhen_huan"},
            {"text": "哈哈，我这是潮流职业装", "persona": "yue_yunpeng"},
            {"text": "您是时尚杂志编辑吗？", "persona": "xiao_s"},
            {"text": "衣服只是外表，重要的是内心", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=19, scene="salary",
        question="发工资了，你发现缴纳的五险一金比合同上写的高",
        options=[
            {"text": "可能是政策调整了，没事", "persona": "sha_seng"},
            {"text": "这个需要给我一个解释", "persona": "hanzawa_naoki"},
            {"text": "我去人事部门问问情况", "persona": "zhen_huan"},
            {"text": "哈哈，这是给我们的惊喜吗", "persona": "yue_yunpeng"},
            {"text": "你们这是明抢啊", "persona": "xiao_s"},
            {"text": "钱赚多少不重要，重要的是心态", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=20, scene="resign",
        question="你决定离职，老板说给你加薪让你留下",
        options=[
            {"text": "那我再考虑考虑", "persona": "sha_seng"},
            {"text": "既然要加薪，为什么不早加", "persona": "hanzawa_naoki"},
            {"text": "感谢您的认可，我需要时间想想", "persona": "zhen_huan"},
            {"text": "哈哈，早知今日，何必当初", "persona": "yue_yunpeng"},
            {"text": "现在加薪？早干什么去了", "persona": "xiao_s"},
            {"text": "人生就是不断的选择，留下也好，走也罢", "persona": "yu_hua"},
        ]
    ),
]


def get_question(question_id: int):
    if 1 <= question_id <= len(QUIZ_QUESTIONS):
        return QUIZ_QUESTIONS[question_id - 1]
    return None


def calculate_persona_scores(answers: list) -> dict:
    scores = {p: 0 for p in PersonaType}
    for i, answer in enumerate(answers):
        if i >= len(QUIZ_QUESTIONS):
            break
        question = QUIZ_QUESTIONS[i]
        idx = ord(answer) - ord('A')
        if 0 <= idx < len(question.options):
            persona_str = question.options[idx].get("persona", "")
            if persona_str:
                try:
                    persona = PersonaType(persona_str)
                    scores[persona] += 1
                except ValueError:
                    pass
    return scores


def get_dominant_persona(scores: dict) -> PersonaType:
    if not scores:
        return PersonaType.SHA_SENG
    max_score = max(scores.values())
    dominant = [p for p, s in scores.items() if s == max_score]
    priority = [
        PersonaType.HANZAWA_NAOKI, PersonaType.ZHEN_HUAN,
        PersonaType.YU_HUA, PersonaType.YUE_YUNPENG,
        PersonaType.XIAO_S, PersonaType.SHA_SENG,
    ]
    for p in priority:
        if p in dominant:
            return p
    return dominant[0]
