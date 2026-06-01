import aiosqlite
from typing import List, Dict, Any, Optional
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
        # Таблица товаров
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price_usd REAL NOT NULL,
                file_content TEXT NOT NULL -- Контент автовыдачи (ссылка/код)
            )
        """)
        # Таблица инвойсов
        await db.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                invoice_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                amount REAL NOT NULL,
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

async def get_products() -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM products") as cursor:
            return [dict(row) for row in await cursor.fetchall()]

async def get_product(product_id: int) -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM products WHERE id = ?", (product_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def create_product(name: str, description: str, price_usd: float, file_content: str):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "INSERT INTO products (name, description, price_usd, file_content) VALUES (?, ?, ?, ?)",
            (name, description, price_usd, file_content)
        )
        await db.commit()

async def delete_product(product_id: int):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        await db.commit()

async def create_invoice(invoice_id: str, user_id: int, product_id: int, amount: float):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "INSERT INTO invoices (invoice_id, user_id, product_id, amount) VALUES (?, ?, ?, ?)",
            (invoice_id, user_id, product_id, amount)
        )
        await db.commit()

async def get_invoice(invoice_id: str) -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM invoices WHERE invoice_id = ?", (invoice_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def update_invoice_status(invoice_id: str, status: str):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            "UPDATE invoices SET status = ? WHERE invoice_id = ?",
            (status, invoice_id)
        )
        await db.commit()
