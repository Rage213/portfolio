FROM python:3.11-slim

WORKDIR /app

# Отключаем буферизацию логов Python (чтобы видеть логи на Render сразу)
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
