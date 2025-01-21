from zhipuai import ZhipuAI
from typing import Dict, Optional

class Summarizer:
    def __init__(self, api_key: str, base_url: str, model: str, temperature: float, max_tokens: int):
        self.client = ZhipuAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def summarize_article(self, article: Dict) -> Optional[str]:
        """生成单篇文章摘要"""
        system_prompt = """
        ## Goals
        读取并解析JSON格式的文章，提炼出文章的主旨，形成一句简洁的概述。

        ## Constrains:
        概述长度不超过80字，保持文章的原意和重点。

        ## Skills
        JSON解析能力，文章内容理解和总结能力。

        ## Output Format
        一句话概述，简洁明了，不超过80字。

        ## Workflow:
        1. 读取并解析JSON格式的文章
        2. 理解文章内容，提取关键信息
        3. 生成一句简洁的概述，不超过80字
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"文章内容：{article}"}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"生成摘要失败: {e}")
            return None
