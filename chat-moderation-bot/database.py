import aiosqlite
from typing import Dict, Any, Optional
from config import DATABASE_URL

async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        # Таблица предупреждений пользователей
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                chat_id INTEGER NOT NULL,
                count INTEGER DEFAULT 0,
                reason TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Таблица настроек чата
        await db.execute("""
            CREATE TABLE IF NOT EXISTS chat_settings (
                chat_id INTEGER PRIMARY KEY,
                welcome_enabled INTEGER DEFAULT 1,
                antispam_enabled INTEGER DEFAULT 1
            )
        """)
        await db.commit()

async def get_warn_count(user_id: int, chat_id: int) -> int:
    async with aiosqlite.connect(DATABASE_URL) as db:
        async with db.execute(
            "SELECT SUM(count) as total FROM warnings WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row and row[0] is not None else 0

async def add_warning(user_id: int, chat_id: int, reason: Optional[str]) -> int:
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "INSERT INTO warnings (user_id, chat_id, count, reason) VALUES (?, ?, 1, ?)",
            (user_id, chat_id, reason)
        )
        await db.commit()
        return await get_warn_count(user_id, chat_id)

async def reset_warnings(user_id: int, chat_id: int):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "DELETE FROM warnings WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id)
        )
        await db.commit()
