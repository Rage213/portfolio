import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import database
import handlers
from scheduler import scheduler, load_scheduled_jobs

logging.basicConfig(level=logging.INFO)

async def main():
    # Инициализация БД
    await database.init_db()

    # Инициализация Бота и Диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(handlers.router)

    # Запускаем планировщик APScheduler
    scheduler.start()
    
    # Загружаем сохраненные задачи в планировщик
    await load_scheduled_jobs(bot)

    print("Auto-Posting Bot started polling...")
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
