from fastapi import APIRouter, HTTPException
import httpx
import requests
from app.models.text import Text
import app.schemas.base_api_response
from app.schemas.base_api_response import SuccessResponse

router = APIRouter()

@router.post("/politically-sensitive")
async def read_root(text: Text):
    # try:
    #     async with httpx.AsyncClient() as client:
    #         payload = {
    #             "model": "deepseek-r1:32b",
    #             "prompt": f'''
    #                 现在你是一名政治家,针对这篇文章:{text.content}
    #                 你觉得有暗含政治违规的内容吗?''',
    #             "stream": False
    #         }
    #         resp = await client.post('http://115.190.111.233:11434/api/generate', json=payload)
    #         print(resp)
    #         if resp.status_code == 200:
    #             return 200
    #         else :
    #             raise HTTPException(status_code=resp.status_code, detail=f"deepseek返回结果非200,报错内容: {resp.text}")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"调用远程deepseek失败: {e}")
    try:
        payload = {
            "model": "gemma3:27b",
            "prompt": f'''
                           现在你是一名政治家,针对这篇文章:{text.content}
                           你觉得有暗含政治敏感的内容吗?''',
            "stream": False
        }
        response = requests.post('http://115.190.29.101:11434/api/generate', json=payload, timeout=1000)
        if response.status_code == 200:
            print(response.json()['response'])
            return SuccessResponse(data=response.json()['response'])
        else:
            print(f"模型接口调用错误,错误码{response.status_code},信息:{response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"模型接口调用错误,错误码{response.status_code},信息:{response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"调用远程模型失败: {e}")
