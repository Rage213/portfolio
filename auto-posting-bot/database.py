import aiosqlite
from typing import List, Dict, Any, Optional
from datetime import datetime
from config import DATABASE_URL

async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                channel_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                username TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                media_id TEXT,
                media_type TEXT, -- 'photo', 'video', None
                channel_id INTEGER NOT NULL,
                scheduled_at TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'scheduled', -- 'scheduled', 'posted', 'failed'
                FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
            )
        """)
        await db.commit()

async def add_channel(channel_id: int, title: str, username: Optional[str]):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "INSERT OR REPLACE INTO channels (channel_id, title, username) VALUES (?, ?, ?)",
            (channel_id, title, username)
        )
        await db.commit()

async def get_channels() -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM channels") as cursor:
            return [dict(row) for row in await cursor.fetchall()]

async def create_post(text: Optional[str], media_id: Optional[str], media_type: Optional[str], channel_id: int, scheduled_at: datetime) -> int:
    async with aiosqlite.connect(DATABASE_URL) as db:
        async with db.execute(
            "INSERT INTO posts (text, media_id, media_type, channel_id, scheduled_at) VALUES (?, ?, ?, ?, ?)",
            (text, media_id, media_type, channel_id, scheduled_at.isoformat())
        ) as cursor:
            post_id = cursor.lastrowid
            await db.commit()
            return post_id

async def get_scheduled_posts() -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT p.*, c.title as channel_title FROM posts p JOIN channels c ON p.channel_id = c.channel_id WHERE p.status = 'scheduled' ORDER BY p.scheduled_at ASC") as cursor:
            return [dict(row) for row in await cursor.fetchall()]

async def update_post_status(post_id: int, status: str):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "UPDATE posts SET status = ? WHERE id = ?",
            (status, post_id)
        )
        await db.commit()
