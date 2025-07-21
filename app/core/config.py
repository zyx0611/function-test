# app/core/config.py
from dotenv import load_dotenv
import os

# 加载一次 dotenv（只在第一次调用时）
load_dotenv()

def get_model_endpoint():
    return os.getenv("MODEL_ENDPOINT", "http://localhost:11434/api/generate")
