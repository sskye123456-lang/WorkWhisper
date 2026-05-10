# LLM Service
import os
from typing import Optional, Dict
from openai import OpenAI

from app.config import config
from app.models.user import PersonaType, ReplySuggestion


class LLMService:
    def __init__(self):
        self.client = None
        self.model = config.OPENAI_MODEL
        self._prompts_cache: Dict[PersonaType, str] = {}
        if config.OPENAI_API_KEY:
            try:
                self.client = OpenAI(
                    api_key=config.OPENAI_API_KEY,
                    base_url=config.OPENAI_BASE_URL,
                )
            except Exception as e:
                print("OpenAI init failed:", e)
                self.client = None
        else:
            print("No OPENAI_API_KEY, using mock mode")

    def load_persona_prompt(self, persona: PersonaType) -> str:
        if persona in self._prompts_cache:
            return self._prompts_cache[persona]
        prompt_path = os.path.join(
            os.path.dirname(__file__), "..", "prompts", persona.value + ".md"
        )
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        else:
            prompt = self._get_default_prompt(persona)
        self._prompts_cache[persona] = prompt
        return prompt

    def _get_default_prompt(self, persona: PersonaType) -> str:
        prompts = {
            PersonaType.SHA_SENG: "You are a peacemaker. Always agree and avoid conflict.",
            PersonaType.HANZAWA_NAOKI: "You are a rebel. Fight back against unfair treatment.",
            PersonaType.ZHEN_HUAN: "You are a diplomat. Give vague but polite responses.",
            PersonaType.YU_HUA: "You are a philosopher. Use humor to defuse tension.",
            PersonaType.YUE_YUNPENG: "You are a comedian. Use self-deprecating humor.",
            PersonaType.XIAO_S: "You are a critic. Give sharp, sarcastic responses.",
        }
        return prompts.get(persona, prompts[PersonaType.SHA_SENG])

    def generate_reply(self, persona: PersonaType, message: str) -> ReplySuggestion:
        system_prompt = self.load_persona_prompt(persona)
        user_prompt = "The colleague said: " + message + "\n\nGenerate 3 reply versions: mild, standard, and fire. Format:\n[MILD]\n...\n[STANDARD]\n...\n[FIRE]\n..."
        
        try:
            if not self.client:
                return self._get_mock_reply(persona, message)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.8,
                max_tokens=1000,
            )
            content = response.choices[0].message.content
            mild, standard, fire = self._parse_reply_versions(content)
            return ReplySuggestion(
                mild=mild, standard=standard, fire=fire,
                persona=persona, original_message=message,
            )
        except Exception as e:
            print("LLM error:", e)
            return self._get_mock_reply(persona, message)

    def _parse_reply_versions(self, content: str):
        import re
        mild = standard = fire = ""
        mild_match = re.search(r"\[MILD\]\s*(.+?)(?=\[STANDARD\]|$)", content, re.DOTALL)
        standard_match = re.search(r"\[STANDARD\]\s*(.+?)(?=\[FIRE\]|$)", content, re.DOTALL)
        fire_match = re.search(r"\[FIRE\]\s*(.+?)$", content, re.DOTALL)
        if mild_match:
            mild = mild_match.group(1).strip()
        if standard_match:
            standard = standard_match.group(1).strip()
        if fire_match:
            fire = fire_match.group(1).strip()
        if not mild:
            mild = "Let me think about this..."
        if not standard:
            standard = "Got it, I will handle it."
        if not fire:
            fire = "I need to check on this."
        return mild, standard, fire

    def _get_mock_reply(self, persona: PersonaType, message: str) -> ReplySuggestion:
        mock_replies = {
            PersonaType.SHA_SENG: ReplySuggestion(
                mild="Okay, sounds good!",
                standard="Sure, I agree with you.",
                fire="You are absolutely right!",
                persona=persona, original_message=message,
            ),
            PersonaType.HANZAWA_NAOKI: ReplySuggestion(
                mild="I have some concerns about this.",
                standard="This does not seem right to me.",
                fire="I cannot accept this. Double payback!",
                persona=persona, original_message=message,
            ),
            PersonaType.ZHEN_HUAN: ReplySuggestion(
                mild="Let me consider this carefully.",
                standard="That is an interesting perspective.",
                fire="I will have to think about how to respond properly.",
                persona=persona, original_message=message,
            ),
            PersonaType.YU_HUA: ReplySuggestion(
                mild="Ha, life is full of surprises.",
                standard="Well, that is one way to look at it.",
                fire="You know what they say about expectations...",
                persona=persona, original_message=message,
            ),
            PersonaType.YUE_YUNPENG: ReplySuggestion(
                mild="Oh wow, you got me there!",
                standard="Haha, okay okay, I hear you!",
                fire="My dear friend, you are too much!",
                persona=persona, original_message=message,
            ),
            PersonaType.XIAO_S: ReplySuggestion(
                mild="Um, okay...",
                standard="What exactly are you trying to say?",
                fire="Seriously? What is wrong with you?",
                persona=persona, original_message=message,
            ),
        }
        return mock_replies.get(persona, mock_replies[PersonaType.SHA_SENG])


llm_service = LLMService()
