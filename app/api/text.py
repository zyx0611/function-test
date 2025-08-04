from fastapi import APIRouter, HTTPException
import requests
from app.models.text import Text
from app.schemas.base_api_response import SuccessResponse
import logging
import asyncio
from app.core.config import get_model_endpoint

router = APIRouter()
logger = logging.getLogger(__name__)

endpoint = get_model_endpoint()

def sync_request_model(payload: dict):
    try:
        response = requests.post(endpoint + '/api/generate', json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"同步模型请求失败: {e}")

@router.post("/politically-sensitive")
async def read_root(text: Text):
    # try:
    #     headers = {
    #         "User-Agent": "python-requests/2.31.0",
    #         "Accept": "*/*",
    #         "Connection": "keep-alive",
    #         "Content-Type": "application/json"
    #     }
    #     async with httpx.AsyncClient(http2=False, timeout=30.0, headers=headers) as client:
    #         payload = {
    #             "model": "gemma3:27b",
    #             "prompt": f'''
    #                 现在你是一名政治家,针对这篇文章:{text.content}
    #                 你觉得有暗含政治违规的内容吗?''',
    #             "stream": False
    #         }
    #         resp = await client.post('http://115.190.111.233:11434/api/generate', json=payload)
    #         content = await resp.aread()
    #         print(content)
    #         if resp.status_code == 200:
    #             return 200
    #         else :
    #             raise HTTPException(status_code=resp.status_code, detail=f"deepseek返回结果非200,报错内容: {resp.text}")
    # except Exception as e:
    #     logger.info(f'线上模型报错内容: {e}')
    #     raise HTTPException(status_code=500, detail=f"调用远程deepseek失败: {e}")
    try:
        payload = {
            "model": "gemma3:27b",
            "prompt": f"""
        你是一个内容审核助手。请分析以下内容是否包含政治违规内容，并以如下 JSON 格式返回：

        {{
          "has_political_violation": true/false,
          "reason": "解释原因"
        }}

        注意：只能返回符合 JSON 语法的内容，不能输出其他内容。

        内容如下：
        {text.content}
        """,
            "stream": False
        }
        # 异步执行同步请求
        result = await asyncio.to_thread(sync_request_model, payload)
        return SuccessResponse(data=result.get("response"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"调用远程模型失败: {e}")
