import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

BOT_TOKEN = BOT_TOKEN or ""
GEMINI_API_KEY = GEMINI_API_KEY or ""
