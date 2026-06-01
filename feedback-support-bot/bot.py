import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import database
import handlers

logging.basicConfig(level=logging.INFO)

async def main():
    # Инициализация асинхронной БД
    await database.init_db()

    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(handlers.router)

    print("Feedback/Support Bot started polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
