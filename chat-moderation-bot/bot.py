import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import database
from handlers import moderation, antispam, welcome

logging.basicConfig(level=logging.INFO)

async def main():
    # Инициализация БД
    await database.init_db()

    # Инициализация Бота и Диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры обработчиков
    # Важен порядок: welcome и antispam должны идти перед модерацией, либо фильтроваться по ролям
    dp.include_router(welcome.router)
    dp.include_router(moderation.router)
    dp.include_router(antispam.router) # Обрабатывает обычные сообщения и чистит спам

    print("Chat Moderation Bot started polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
