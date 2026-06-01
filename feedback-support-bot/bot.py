import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_impl import SimpleRequestHandler, setup_application
from aiohttp import web

from config import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT
import database
import handlers

logging.basicConfig(level=logging.INFO)

async def on_startup(bot: Bot) -> None:
    # Инициализация БД
    await database.init_db()
    
    if WEBHOOK_HOST:
        webhook_url = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
        logging.info(f"Setting webhook to: {webhook_url}")
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=["message", "callback_query"]
        )
    else:
        logging.info("Starting bot in local POLLING mode...")

async def main_polling():
    await database.init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    print("Feedback/Support Bot started polling...")
    await dp.start_polling(bot)

def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers.router)
    
    dp.startup.register(on_startup)
    
    if WEBHOOK_HOST:
        # Режим Вебхуков для Render.com
        app = web.Application()
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    else:
        # Локальный режим Polling
        asyncio.run(main_polling())

if __name__ == "__main__":
    main()
