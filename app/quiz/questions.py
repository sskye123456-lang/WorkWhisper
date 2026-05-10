# Quiz Questions
from app.models.user import QuizQuestion, PersonaType

QUIZ_QUESTIONS = [
    QuizQuestion(
        id=1, scene="meeting", question="Boss asks: Any questions?",
        options=[
            {"text": "No questions", "persona": "sha_seng"},
            {"text": "I have suggestions", "persona": "hanzawa_naoki"},
            {"text": "Let me think", "persona": "zhen_huan"},
            {"text": "Haha interesting", "persona": "yue_yunpeng"},
            {"text": "What is the point?", "persona": "xiao_s"},
            {"text": "Life goes on", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=2, scene="deadline", question="Colleague says: Can you finish by today?",
        options=[
            {"text": "Sure no problem", "persona": "sha_seng"},
            {"text": "That is not fair", "persona": "hanzawa_naoki"},
            {"text": "Let me check my schedule", "persona": "zhen_huan"},
            {"text": "Oh you are killing me!", "persona": "yue_yunpeng"},
            {"text": "Are you serious?", "persona": "xiao_s"},
            {"text": "We all die eventually", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=3, scene="feedback", question="Boss gives harsh feedback",
        options=[
            {"text": "Thank you for the feedback", "persona": "sha_seng"},
            {"text": "I disagree with this", "persona": "hanzawa_naoki"},
            {"text": "I appreciate your perspective", "persona": "zhen_huan"},
            {"text": "Wow you really got me!", "persona": "yue_yunpeng"},
            {"text": "Excuse me?", "persona": "xiao_s"},
            {"text": "Pain is part of life", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=4, scene="overtime", question="Asked to work overtime on weekend",
        options=[
            {"text": "Okay I will do it", "persona": "sha_seng"},
            {"text": "This is unacceptable", "persona": "hanzawa_naoki"},
            {"text": "Let me see if I can", "persona": "zhen_huan"},
            {"text": "My weekend! Nooo!", "persona": "yue_yunpeng"},
            {"text": "You must be joking", "persona": "xiao_s"},
            {"text": "Rest is for the weak", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=5, scene="credit", question="Colleague takes credit for your work",
        options=[
            {"text": "It is okay, team effort", "persona": "sha_seng"},
            {"text": "That was actually my work", "persona": "hanzawa_naoki"},
            {"text": "Glad the project succeeded", "persona": "zhen_huan"},
            {"text": "Oh you did that? Amazing!", "persona": "yue_yunpeng"},
            {"text": "Excuse me, what?", "persona": "xiao_s"},
            {"text": "Nothing really belongs to us", "persona": "yu_hua"},
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
