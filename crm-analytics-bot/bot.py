import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
import database
import handlers

async def main():
    # 1. Initialize SQLite Database
    await database.init_db()
    
    # 2. Setup Bot & Dispatcher
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # 3. Include Routers
    dp.include_router(handlers.router)
    
    print("=" * 60)
    print("Starting Nexus Labs CRM & Analytics Bot...")
    print(f"Configured Admin ID: {config.ADMIN_ID}")
    print("=" * 60)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
