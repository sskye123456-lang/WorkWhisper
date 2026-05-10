# Card Builder
import json
from typing import Optional, Dict, List
from app.models.user import PersonaType, PERSONAS, ReplySuggestion
from app.quiz.questions import QuizQuestion
from app.config import config


class CardBuilder:
    @staticmethod
    def welcome_card() -> dict:
        return {
            "type": "template",
            "data": {
                "template_id": "AAqkjm8KABY",
                "template_variable": {
                    "title": "Welcome to Workplace Mouthpiece",
                    "content": "I help you reply to colleagues with style! Start the quiz to find your persona.",
                }
            }
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
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "Q" + str(question.id) + ": " + question.question[:50]}},
            "elements": elements
        }

    @staticmethod
    def quiz_result_card(persona: PersonaType, scores: dict) -> dict:
        p = PERSONAS[persona]
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": p.emoji + " " + p.title},
                "template": p.header_template
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "**" + p.quote + "**"}},
                {"tag": "div", "text": {"tag": "lark_md", "content": p.description}},
                {"tag": "action", "actions": [
                    {"tag": "button", "text": {"content": "Start Using", "tag": "plain_text"},
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
            "header": {"title": {"tag": "plain_text", "content": "Choose Your Persona"}},
            "elements": [{"tag": "action", "actions": elements}]
        }

    @staticmethod
    def reply_card(suggestion: ReplySuggestion, original_message: str, remaining: int = 3) -> dict:
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "Reply Suggestions"}, "template": "blue"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "**Mild:**\n" + suggestion.mild}},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**Standard:**\n" + suggestion.standard}},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**Fire:**\n" + suggestion.fire}},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "Reinforcements left: " + str(remaining)}]}
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
            "header": {"title": {"tag": "plain_text", "content": "Call Reinforcement (" + str(remaining) + " left)"}},
            "elements": [{"tag": "action", "actions": elements}] if elements else [{"tag": "div", "text": {"tag": "plain_text", "content": "No other personas available"}}]
        }

    @staticmethod
    def reinforcement_exhaust_card() -> dict:
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "No Reinforcements Left"}, "template": "red"},
            "elements": [{"tag": "div", "text": {"tag": "plain_text", "content": "You have used all your daily reinforcements. Try again tomorrow!"}}]
        }

    @staticmethod
    def help_card() -> dict:
        return {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "Help - Workplace Mouthpiece"}, "template": "blue"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "**How to use:**\n1. Send any message to start\n2. I will generate 3 reply versions\n3. Choose the one you like!"}},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**Commands:**\n- help: Show this help\n- switch: Change persona\n- test: Retake quiz"}},
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
