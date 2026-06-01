import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Simple validation
if not BOT_TOKEN:
    BOT_TOKEN = "MOCK_TOKEN_FOR_VERIFICATION"

if not GEMINI_API_KEY:
    GEMINI_API_KEY = "MOCK_KEY_FOR_VERIFICATION"
