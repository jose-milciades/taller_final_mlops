FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/artifacts/model.onnx \
    PORT=8080

WORKDIR /app

COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir ".[cloud]"

COPY app ./app
COPY artifacts ./artifacts

EXPOSE 8080

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
