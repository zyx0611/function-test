FROM python:3.11-slim

WORKDIR /app

COPY . .

# 安装 uv（或 poetry）用于解析 pyproject.toml
RUN pip install uv

# 安装 pyproject.toml 中的依赖
RUN uv pip install --system --requirements requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
