import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import database
from handlers import user, admin

logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize Database
    await database.init_db()

    # Initialize Bot & Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Register routers
    dp.include_router(admin.router)
    dp.include_router(user.router)

    # Start polling
    print("Bot started polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
