from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from aiogram import Bot
from datetime import datetime
import logging
import database

logger = logging.getLogger("scheduler")

# Инициализируем планировщик
scheduler = AsyncIOScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
)

async def send_scheduled_post(bot: Bot, post_id: int, channel_id: int, text: str, media_id: str, media_type: str):
    """Задача отправки поста в канал"""
    try:
        if media_type == "photo":
            await bot.send_photo(chat_id=channel_id, photo=media_id, caption=text)
        elif media_type == "video":
            await bot.send_video(chat_id=channel_id, video=media_id, caption=text)
        else:
            await bot.send_message(chat_id=channel_id, text=text)
            
        await database.update_post_status(post_id, "posted")
        logger.info(f"Post {post_id} successfully sent to channel {channel_id}")
    except Exception as e:
        await database.update_post_status(post_id, "failed")
        logger.error(f"Failed to send scheduled post {post_id}: {e}")

def schedule_post(bot: Bot, post_id: int, channel_id: int, text: str, media_id: str, media_type: str, run_date: datetime):
    """Регистрирует новую задачу отправки в планировщике"""
    scheduler.add_job(
        send_scheduled_post,
        'date',
        run_date=run_date,
        args=[bot, post_id, channel_id, text, media_id, media_type],
        id=f"post_{post_id}"
    )

async def load_scheduled_jobs(bot: Bot):
    """Загружает запланированные посты при старте бота"""
    # Удаляем устаревшие задачи из APScheduler во избежание дублирования
    scheduler.remove_all_jobs()
    
    posts = await database.get_scheduled_posts()
    now = datetime.now()
    
    for post in posts:
        run_date = datetime.fromisoformat(post["scheduled_at"])
        if run_date > now:
            schedule_post(
                bot=bot,
                post_id=post["id"],
                channel_id=post["channel_id"],
                text=post["text"],
                media_id=post["media_id"],
                media_type=post["media_type"],
                run_date=run_date
            )
        else:
            # Если время отправки прошло, пока бот был выключен
            await database.update_post_status(post["id"], "failed")
