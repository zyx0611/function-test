from fastapi import FastAPI
from app.api import text
import uvicorn

app = FastAPI()

app.include_router(text.router, prefix="/text", tags=["text"])

@app.get('/')
def in_function_text():
    return '靓仔,今天也要记得抽烟哦!!!'

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=1022)