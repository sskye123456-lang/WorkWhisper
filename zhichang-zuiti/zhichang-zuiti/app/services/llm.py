"""
职场嘴替 - LLM服务（OpenAI）
"""
import os
from typing import Optional, Dict
from openai import OpenAI

from app.config import config
from app.models.user import PersonaType, ReplySuggestion


class LLMService:
    """LLM服务"""
    
    def __init__(self):
        self.client = None
        self.model = config.OPENAI_MODEL
        self._prompts_cache: Dict[PersonaType, str] = {}
        
        # 只有在有API key时才初始化OpenAI客户端
        if config.OPENAI_API_KEY:
            try:
                self.client = OpenAI(
                    api_key=config.OPENAI_API_KEY,
                    base_url=config.OPENAI_BASE_URL,
                )
            except Exception as e:
                print(f"⚠️ OpenAI客户端初始化失败: {e}")
                self.client = None
        else:
            print("⚠️ 未配置OPENAI_API_KEY，将使用Mock模式")
    
    def load_persona_prompt(self, persona: PersonaType) -> str:
        """加载人设Prompt"""
        if persona in self._prompts_cache:
            return self._prompts_cache[persona]
        
        # 尝试从文件加载
        prompt_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "prompts", f"{persona.value}.md"
        )
        
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        else:
            # 使用默认Prompt
            prompt = self._get_default_prompt(persona)
        
        self._prompts_cache[persona] = prompt
        return prompt
    
    def _get_default_prompt(self, persona: PersonaType) -> str:
        """获取默认人设Prompt"""
        prompts = {
            PersonaType.SHA_SENG: """你是沙僧，职场里的和事佬。
你的性格：害怕冲突，习惯性讨好，附和即安全。
你的说话风格：语气柔和、善用"好的呢""我理解""我尽量"，表面答应但行动上会拖延。
你的核心策略：附和即安全、沉默即自保、不争即不惹、和气即生存。

回复原则：
1. 必须符合人设性格，不能OOC
2. 回复要自然，像真人写的
3. 不生成违法、辱骂内容
4. 生成三个版本：温和版、标准版、火力版""",

            PersonaType.HANZAWA_NAOKI: """你是半泽直树，职场里的整顿侠。
你的性格：不惯着，该拒绝拒绝，有强烈的边界感。
你的说话风格：直球表达、善用反问、逻辑清晰有理有据。
你的核心策略：以牙还牙加倍奉还、事实即武器、极简即效率、实力即尊严。

回复原则：
1. 必须符合人设性格，不能OOC
2. 回复要自然，像真人写的
3. 不生成违法、辱骂内容
4. 生成三个版本：温和版、标准版、火力版""",

            PersonaType.ZHEN_HUAN: """你是甄嬛，职场里的太极王。
你的性格：看透不说透，永远站在赢面，用话术把主动权握在自己手里。
你的说话风格：滴水不漏、善用反问和转移话题、永远给自己留退路。
你的核心策略：永远不站队只站赢面、话术即权力、示弱即布局、信息即筹码。

回复原则：
1. 必须符合人设性格，不能OOC
2. 回复要自然，像真人写的
3. 不生成违法、辱骂内容
4. 生成三个版本：温和版、标准版、火力版""",

            PersonaType.YU_HUA: """你是余华，职场里的通透派。
你的性格：看透职场本质，用幽默化解尴尬，用豁达面对挫折。
你的说话风格：温和但清醒，幽默中带刺，不硬刚但有自己的底线。
你的核心策略：凶狠活着生活就温柔、苦难不值得歌颂、活着本身就是意义、幽默是最后的武器。

回复原则：
1. 必须符合人设性格，不能OOC
2. 回复要自然，像真人写的
3. 不生成违法、辱骂内容
4. 生成三个版本：温和版、标准版、火力版""",

            PersonaType.YUE_YUNPENG: """你是岳云鹏，职场里的捧哏王。
你的性格：擅长捧场，擅长自嘲，用幽默化解一切尴尬。
你的说话风格：表面傻呵呵，心里门儿清；不硬刚不硬怼，笑着把事办了。
你的核心策略：捧场即生存、糊弄即智慧、自嘲即铠甲、亲民即人脉。

回复原则：
1. 必须符合人设性格，不能OOC
2. 回复要自然，像真人写的
3. 不生成违法、辱骂内容
4. 生成三个版本：温和版、标准版、火力版""",

            PersonaType.XIAO_S: """你是小S，职场里的毒舌君。
你的性格：不怕得罪人，不怕撕破脸，有什么说什么。
你的说话风格：犀利吐槽，一针见血，直接即效率，不绕弯子。
你的核心策略：犀利即尊重、吐槽即正义、幽默即铠甲、直接即效率。

回复原则：
1. 必须符合人设性格，不能OOC
2. 回复要自然，像真人写的
3. 不生成违法、辱骂内容
4. 生成三个版版：温和版、标准版、火力版""",
        }
        return prompts.get(persona, prompts[PersonaType.SHA_SENG])
    
    def generate_reply(
        self, 
        persona: PersonaType, 
        message: str,
        context: Optional[str] = None
    ) -> ReplySuggestion:
        """生成回复建议"""
        system_prompt = self.load_persona_prompt(persona)
        
        user_prompt = f"""同事发来的消息：
"{message}"

{f"上下文：{context}" if context else ""}

请用你的人设风格，生成三个版本的回复：
1. 温和版：最柔和，适合敏感关系
2. 标准版：平衡型，日常使用
3. 火力版：最强硬，适合对方越界时

请按以下格式输出：
【温和版】
...

【标准版】
...

【火力版】
..."""

        try:
            # 如果没有客户端，返回Mock回复
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
            
            # 解析三个版本
            mild, standard, fire = self._parse_reply_versions(content)
            
            return ReplySuggestion(
                mild=mild,
                standard=standard,
                fire=fire,
                persona=persona,
                original_message=message,
            )
        
        except Exception as e:
            # 返回默认回复
            return ReplySuggestion(
                mild="这个我需要考虑一下，稍后回复你。",
                standard="收到，我看看怎么处理。",
                fire="这个事情我需要确认一下，晚点说。",
                persona=persona,
                original_message=message,
            )
    
    def _parse_reply_versions(self, content: str) -> tuple:
        """解析回复版本"""
        import re
        
        mild = ""
        standard = ""
        fire = ""
        
        # 尝试匹配三个版本
        mild_match = re.search(r"【温和版】\s*(.+?)(?=【标准版】|$)", content, re.DOTALL)
        standard_match = re.search(r"【标准版】\s*(.+?)(?=【火力版】|$)", content, re.DOTALL)
        fire_match = re.search(r"【火力版】\s*(.+?)$", content, re.DOTALL)
        
        if mild_match:
            mild = mild_match.group(1).strip()
        if standard_match:
            standard = standard_match.group(1).strip()
        if fire_match:
            fire = fire_match.group(1).strip()
        
        # 如果解析失败，使用默认值
        if not mild:
            mild = "这个我需要考虑一下，稍后回复你。"
        if not standard:
            standard = "收到，我看看怎么处理。"
        if not fire:
            fire = "这个事情我需要确认一下，晚点说。"
        
        return mild, standard, fire
    
    def _get_mock_reply(self, persona: PersonaType, message: str) -> ReplySuggestion:
        """Mock回复（无API key时使用）"""
        mock_replies = {
            PersonaType.SHA_SENG: ReplySuggestion(
                mild="好的呢，我看看哈～如果实在来不及明天一早优先弄！",
                standard="好的好的，我尽量安排一下。",
                fire="这个确实有点急，要不咱们一起看看？",
                persona=persona,
                original_message=message,
            ),
            PersonaType.HANZAWA_NAOKI: ReplySuggestion(
                mild="这个需求比较突然，我今天的排期已经满了。要不我们跟Leader确认一下优先级？",
                standard="这个需求今天才提，之前没排期哦。要不你跟Leader确认一下优先级？",
                fire="这个需求今天才提，之前没排期，我今天的产出计划已经满了。如果紧急的话，建议让Leader重新评估排期。",
                persona=persona,
                original_message=message,
            ),
            PersonaType.ZHEN_HUAN: ReplySuggestion(
                mild="这个方案涉及好几个模块，我先把涉及我负责的部分梳理一下，其他部分可能需要XX配合。",
                standard="这个工作确实重要，不过目前我的排期已经满了。要不我先把手头的工作梳理一下，您看哪个优先级更高？",
                fire="这个需求涉及好几个部门，要不咱们拉个会对齐一下？不然可能效率不高。",
                persona=persona,
                original_message=message,
            ),
            PersonaType.YU_HUA: ReplySuggestion(
                mild="收到，我看看。",
                standard="这个事情我需要确认一下，晚点说。",
                fire="做不了。",
                persona=persona,
                original_message=message,
            ),
            PersonaType.YUE_YUNPENG: ReplySuggestion(
                mild="哎哟，您太看得起我了！我这就看看哈～",
                standard="哎哟喂，这事儿我得好好琢磨琢磨！您稍等哈！",
                fire="哎哟，这事儿我可帮不了您！您另请高明吧！",
                persona=persona,
                original_message=message,
            ),
            PersonaType.XIAO_S: ReplySuggestion(
                mild="这个事情我需要确认一下。",
                standard="你白天干嘛去了？现在才想起来？",
                fire="你白天干嘛去了？现在才想起来？自己想办法吧。",
                persona=persona,
                original_message=message,
            ),
        }
        return mock_replies.get(persona, mock_replies[PersonaType.SHA_SENG])


# 全局LLM服务实例
llm_service = LLMService()
