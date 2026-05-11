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
            mild = "这个我要考虑一下..."
        if not standard:
            standard = "收到了，我来处理。"
        if not fire:
            fire = "这个事我需要确认一下。"
        return mild, standard, fire

    def _get_mock_reply(self, persona: PersonaType, message: str) -> ReplySuggestion:
        mock_replies = {
            PersonaType.SHA_SENG: ReplySuggestion(
                mild="好的好的，没问题！",
                standard="行行，我赚同意。",
                fire="你说得对！我全力配合！",
                persona=persona, original_message=message,
            ),
            PersonaType.HANZAWA_NAOKI: ReplySuggestion(
                mild="这个我有些疑问。",
                standard="这样做不太合适吧。",
                fire="我无法接受！要加倍奉还！",
                persona=persona, original_message=message,
            ),
            PersonaType.ZHEN_HUAN: ReplySuggestion(
                mild="让我好好想想。",
                standard="这是个有趣的观点。",
                fire="这个问题我得好好思量一下。",
                persona=persona, original_message=message,
            ),
            PersonaType.YU_HUA: ReplySuggestion(
                mild="哈，人生就是这样。",
                standard="这也是一种看法吧。",
                fire="你知道吗，期待和现实总有落差。",
                persona=persona, original_message=message,
            ),
            PersonaType.YUE_YUNPENG: ReplySuggestion(
                mild="哎呦，这个我服！",
                standard="哈哈哈，行行行，我听到了！",
                fire="我的好朋友，你这是要命啊！",
                persona=persona, original_message=message,
            ),
            PersonaType.XIAO_S: ReplySuggestion(
                mild="啧，这……",
                standard="你到底要说什么？",
                fire="看看你在说什么鬼话？",
                persona=persona, original_message=message,
            ),
        }
        return mock_replies.get(persona, mock_replies[PersonaType.SHA_SENG])


llm_service = LLMService()
