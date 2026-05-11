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
            mild = "\u8fd9\u4e2a\u6211\u8981\u8003\u8651\u4e00\u4e0b..."
        if not standard:
            standard = "\u6536\u5230\u4e86\uff0c\u6211\u6765\u5904\u7406。"
        if not fire:
            fire = "\u8fd9\u4e2a\u4e8b\u6211\u9700\u8981\u786e\u8ba4\u4e00\u4e0b\u3002"
        return mild, standard, fire

    def _get_mock_reply(self, persona: PersonaType, message: str) -> ReplySuggestion:
        mock_replies = {
            PersonaType.SHA_SENG: ReplySuggestion(
                mild="\u597d\u7684\u597d\u7684\uff0c\u6ca1\u95ee\u9898\uff01",
                standard="\u884c\u884c\uff0c\u6211\u8d5a\u540c\u610f\u3002",
                fire="\u4f60\u8bf4\u5f97\u5bf9\uff01\u6211\u5168\u529b\u914d\u5408\uff01",
                persona=persona, original_message=message,
            ),
            PersonaType.HANZAWA_NAOKI: ReplySuggestion(
                mild="\u8fd9\u4e2a\u6211\u6709\u4e9b\u7591\u95ee\u3002",
                standard="\u8fd9\u6837\u505a\u4e0d\u592a\u5408\u9002\u5427\u3002",
                fire="\u6211\u65e0\u6cd5\u63a5\u53d7\uff01\u8981\u52a0\u500d\u5949\u8fd8\uff01",
                persona=persona, original_message=message,
            ),
            PersonaType.ZHEN_HUAN: ReplySuggestion(
                mild="\u8ba9\u6211\u597d\u597d\u60f3\u60f3\u3002",
                standard="\u8fd9\u662f\u4e2a\u6709\u8da3\u7684\u89c2\u70b9\u3002",
                fire="\u8fd9\u4e2a\u95ee\u9898\u6211\u5f97\u597d\u597d\u601d\u91cf\u4e00\u4e0b\u3002",
                persona=persona, original_message=message,
            ),
            PersonaType.YU_HUA: ReplySuggestion(
                mild="\u54c8\uff0c\u4eba\u751f\u5c31\u662f\u8fd9\u6837\u3002",
                standard="\u8fd9\u4e5f\u662f\u4e00\u79cd\u770b\u6cd5\u5427\u3002",
                fire="\u4f60\u77e5\u9053\u5417\uff0c\u671f\u5f85\u548c\u73b0\u5b9e\u603b\u6709\u843d\u5dee\u3002",
                persona=persona, original_message=message,
            ),
            PersonaType.YUE_YUNPENG: ReplySuggestion(
                mild="\u54ce\u5466\uff0c\u8fd9\u4e2a\u6211\u670d\uff01",
                standard="\u54c8\u54c8\uff0c\u884c\u884c\u884c\uff0c\u6211\u542c\u5230\u4e86\uff01",
                fire="\u6211\u7684\u597d\u670b\u53cb\uff0c\u4f60\u8fd9\u662f\u8981\u547d\u554a\uff01",
                persona=persona, original_message=message,
            ),
            PersonaType.XIAO_S: ReplySuggestion(
                mild="\u562c\uff0c\u8fd9\u2026\u2026",
                standard="\u4f60\u5230\u5e95\u8981\u8bf4\u4ec0\u4e48\uff1f",
                fire="\u770b\u770b\u4f60\u5728\u8bf4\u4ec0\u4e48\u9b3c\u8bdd\uff1f",
                persona=persona, original_message=message,
            ),
        }
        return mock_replies.get(persona, mock_replies[PersonaType.SHA_SENG])


llm_service = LLMService()
