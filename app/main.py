from fastapi import FastAPI
from app.api import text
import uvicorn
from dotenv import load_dotenv

app = FastAPI()

app.include_router(text.router, prefix="/text", tags=["text"])

load_dotenv()  # 会自动加载根目录下的 .env 文件

@app.get('/')
def in_function_text():
    return '靓仔,今天也要记得抽烟哦!!!'

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=1022)