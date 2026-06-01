import os
from dotenv import load_dotenv

# Load variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID_RAW = os.getenv("ADMIN_ID", "0")

try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except ValueError:
    ADMIN_ID = 0

# Mock credentials for test safety
if not BOT_TOKEN:
    BOT_TOKEN = "MOCK_TOKEN"
