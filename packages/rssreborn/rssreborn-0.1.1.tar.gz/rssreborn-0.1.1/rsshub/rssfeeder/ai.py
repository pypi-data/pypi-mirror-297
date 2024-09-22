"""
Simple LLM calling
"""

from typing import Any
import openai


class BaseAgent:

    def __init__(self) -> None:
        self.client = openai.Client(
            base_url="http://g.manaai.cn:8082/v1",
            # api_key="sk-8c945794b98ab61cca14a7ecea0df7bf",
            api_key="sk-6baf45798712e0467d616f4fabff0c51",
        )

    def get_response(self, text) -> Any:
        completion = self.client.chat.completions.create(
            model="qwen2-7b",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{text}",
                        }
                    ],
                },
            ],
            stream=False,
        )
        return completion.choices[0].message.content


import json
import textwrap
import re


class NewsAgent(BaseAgent):

    def __init__(self) -> None:
        super().__init__()

        self.summary_prompt = textwrap.dedent(
            """你是一个新闻总结专家，请根据这个content总结一下核心内容，要求：
        - 言简意赅，重点信息突出；
        - 合理使用Mark down语法排版；
        - 字数在50字以内
        新闻内容如下：
        """
        )

        self.tags_prompt = textwrap.dedent(
            """你是新闻分类专家，请根据新闻内容给新闻提出2-4个标签，要求：
        - 输出json，格式为:[{"name": "xxx"}, {"name": "xxx"},...] ；
        - 标签第一个为新闻类别，例如时政、体育、娱乐、经济等；
        - 其他标签要突出新闻主体，例如人物、地点、事件；
        - 每个标签字数在4个字以内；
        - 标签数量不要超过4个；
        新闻内容如下：
        """
        )

    def get_summary(self, text):
        a = self.get_response(f"{self.summary_prompt}\n{text}")
        return a

    def get_tags(self, text):
        a = self.get_response(f"{self.tags_prompt}\n{text}")
        pattern = re.compile(r"(?s)(?:```json\n)?(\[.*?\])")
        match = pattern.search(a)
        if match:
            try:
                a = match.group(1)
                b = json.loads(a)
                b = ",".join([list(i.values())[0] for i in b])
            except Exception as e:
                print(f"json parse error: {a} {e}")
                b = ""
        else:
            b = ""
        return b
