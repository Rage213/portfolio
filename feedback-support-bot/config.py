import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
DATABASE_URL = "support.db"

# Настройки Вебхука для бесплатного деплоя на Render
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL") # Автоматически предоставляется сервисом Render
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = int(os.getenv("PORT", 8080)) # Порт, который Render выделяет при запуске
