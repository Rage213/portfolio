import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) # ID администратора, получающего заявки
DATABASE_URL = "support.db"
