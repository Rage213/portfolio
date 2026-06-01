import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "1800"))
DB_FILE = os.getenv("DB_FILE", "price_history.json")

# Default URLs to track if user doesn't specify others
# Using public/demo mock endpoints for reliable demo testing
TRACKED_PRODUCTS = [
    {
        "id": "book_python",
        "name": "Изучаем Python (Марк Лутц) - Книга",
        "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    },
    {
        "id": "course_python",
        "name": "Курс Python Developer Pro",
        "url": "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
    }
]
