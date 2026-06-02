import aiosqlite
from typing import Dict, Any, Optional, List
from config import DATABASE_URL

async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        # Таблица пользователей
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Таблица обращений (тикетов)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                status TEXT DEFAULT 'open', -- 'open', 'resolved'
                admin_msg_id INTEGER, -- ID пересланного админу сообщения для авто-реплая
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def add_user(user_id: int, username: Optional[str]):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        await db.commit()

async def create_ticket(user_id: int, text: str) -> int:
    async with aiosqlite.connect(DATABASE_URL) as db:
        async with db.execute(
            "INSERT INTO tickets (user_id, text) VALUES (?, ?)",
            (user_id, text)
        ) as cursor:
            ticket_id = cursor.lastrowid
            await db.commit()
            return ticket_id

async def update_ticket_admin_msg(ticket_id: int, admin_msg_id: int):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "UPDATE tickets SET admin_msg_id = ? WHERE id = ?",
            (admin_msg_id, ticket_id)
        )
        await db.commit()

async def get_ticket_by_admin_msg(admin_msg_id: int) -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM tickets WHERE admin_msg_id = ?", (admin_msg_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def close_ticket(ticket_id: int):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "UPDATE tickets SET status = 'resolved' WHERE id = ?",
            (ticket_id,)
        )
        await db.commit()

async def get_ticket(ticket_id: int) -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

