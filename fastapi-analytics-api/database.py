import aiosqlite
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from config import settings

async def init_db():
    async with aiosqlite.connect(settings.DATABASE_URL.replace("sqlite+aiosqlite:///./", "")) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                details TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_bot_event ON events (bot_id, event_type)
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON events (timestamp)
        """)
        await db.commit()

async def log_event(bot_id: int, user_id: int, event_type: str, details: Optional[str] = None):
    async with aiosqlite.connect(settings.DATABASE_URL.replace("sqlite+aiosqlite:///./", "")) as db:
        await db.execute(
            "INSERT INTO events (bot_id, user_id, event_type, details, timestamp) VALUES (?, ?, ?, ?, ?)",
            (bot_id, user_id, event_type, details, datetime.utcnow().isoformat())
        )
        await db.commit()

async def get_bot_metrics(bot_id: int, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    async with aiosqlite.connect(settings.DATABASE_URL.replace("sqlite+aiosqlite:///./", "")) as db:
        db.row_factory = aiosqlite.Row
        
        # Общая статистика
        async with db.execute(
            """
            SELECT 
                COUNT(*) as total_events,
                COUNT(DISTINCT user_id) as active_users
            FROM events 
            WHERE bot_id = ? AND timestamp BETWEEN ? AND ?
            """,
            (bot_id, start_date.isoformat(), end_date.isoformat())
        ) as cursor:
            row = await cursor.fetchone()
            total_events = row["total_events"] if row else 0
            active_users = row["active_users"] if row else 0

        # Статистика по типам событий
        async with db.execute(
            """
            SELECT event_type, COUNT(*) as count 
            FROM events 
            WHERE bot_id = ? AND timestamp BETWEEN ? AND ?
            GROUP BY event_type
            """,
            (bot_id, start_date.isoformat(), end_date.isoformat())
        ) as cursor:
            event_breakdown = {row["event_type"]: row["count"] for row in await cursor.fetchall()}

        # График активности пользователей по дням
        async with db.execute(
            """
            SELECT strftime('%Y-%m-%d', timestamp) as date, COUNT(*) as count
            FROM events
            WHERE bot_id = ? AND timestamp BETWEEN ? AND ?
            GROUP BY date
            ORDER BY date ASC
            """,
            (bot_id, start_date.isoformat(), end_date.isoformat())
        ) as cursor:
            activity_over_time = {row["date"]: row["count"] for row in await cursor.fetchall()}

        return {
            "bot_id": bot_id,
            "total_events": total_events,
            "active_users": active_users,
            "event_breakdown": event_breakdown,
            "activity_over_time": activity_over_time
        }

async def get_system_stats(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    async with aiosqlite.connect(settings.DATABASE_URL.replace("sqlite+aiosqlite:///./", "")) as db:
        db.row_factory = aiosqlite.Row
        
        async with db.execute(
            """
            SELECT 
                COUNT(*) as total_events,
                COUNT(DISTINCT bot_id) as active_bots,
                COUNT(DISTINCT user_id) as total_users
            FROM events
            WHERE timestamp BETWEEN ? AND ?
            """,
            (start_date.isoformat(), end_date.isoformat())
        ) as cursor:
            row = await cursor.fetchone()
            return {
                "total_events": row["total_events"] if row else 0,
                "active_bots": row["active_bots"] if row else 0,
                "total_users": row["total_users"] if row else 0
            }
