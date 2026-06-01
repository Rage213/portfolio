import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

try:
    PRICE_CHANGE_THRESHOLD_PERCENT = float(os.getenv("PRICE_CHANGE_THRESHOLD_PERCENT", 0.05))
except (TypeError, ValueError):
    PRICE_CHANGE_THRESHOLD_PERCENT = 0.05

# Setup defaults if missing for local validation
if not TELEGRAM_BOT_TOKEN:
    TELEGRAM_BOT_TOKEN = "MOCK_TOKEN"
if not TELEGRAM_CHAT_ID:
    TELEGRAM_CHAT_ID = "MOCK_CHAT_ID"
