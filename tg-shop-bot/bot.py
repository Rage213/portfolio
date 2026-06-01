import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import router
import database as db

async def main():
    # Setup logging to stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    if not BOT_TOKEN:
        logging.critical("BOT_TOKEN is empty! Please configure it in .env file.")
        return

    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register handlers router
    dp.include_router(router)

    # Initialize database and populate default products
    logging.info("Initializing SQLite database...")
    await db.init_db()
    
    # Clear any pending updates and start polling
    logging.info("Clearing updates queue and starting bot polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
