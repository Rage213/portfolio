import os
from dotenv import load_dotenv

# Load variables from .env file if it exists
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", "shop_database.db")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    print("Warning: BOT_TOKEN is not set in environment or .env file!")
