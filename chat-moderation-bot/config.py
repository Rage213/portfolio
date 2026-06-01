import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0")) # Канал/группа для логов модерации
SPAM_THRESHOLD = int(os.getenv("SPAM_THRESHOLD", "5")) # Кол-во сообщений за 5 сек для детекта флуда
DATABASE_URL = "moderation.db"
