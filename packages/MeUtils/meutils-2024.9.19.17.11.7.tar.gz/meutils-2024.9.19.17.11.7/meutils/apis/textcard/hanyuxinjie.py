#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : hanyuxinjie
# @Time         : 2024/9/18 13:30
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

BASE_URL = 'https://xy.siliconflow.cn'

HTML_PARSER = re.compile(r'```html(.*?)```', re.DOTALL)


# s = """
# 这是一堆文本
# ```html
# 这是一段html
# ```
# 这是一堆文本
# """
#
# print(HTML_PARSER.findall(s))


async def create(
        text: str = '996',
        model: str = "Pro/THUDM/glm-4-9b-chat",
):
    """
    "Pro/THUDM/glm-4-9b-chat"
    "Qwen/Qwen2-Math-72B-Instruct"
    “deepseek-ai/DeepSeek-V2.5”
    """
    payload = {
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ],
        # "chat_id": "i8yw46k",
        "model": model
    }
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=300) as client:
        async with client.stream(method="POST", url="/api/chat", json=payload) as response:
            # logger.debug(response.status_code)
            async for chunk in response.aiter_lines():
                # for chunk in "response.aiter_lines()":
                yield chunk.replace("智说新语", "汉语新解")


if __name__ == '__main__':
    pass

    arun(create(text="火宝", model="Qwen/Qwen2-Math-72B-Instruct"))
    # arun(main(create(text="火宝", model="Qwen/Qwen2-Math-72B-Instruct", stream=True)))
