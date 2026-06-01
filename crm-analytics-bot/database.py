import os
import aiosqlite
from datetime import datetime, timedelta
import random

DB_PATH = "crm_database.db"

async def init_db():
    """Initializes SQLite tables and inserts mock data for stats graphs if empty."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Create users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create sales table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                product_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.commit()
        
        # Populating historical mock data if empty
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        count = (await cursor.fetchone())[0]
        
        if count == 0:
            print("Populating CRM database with historical mock data...")
            now = datetime.now()
            
            # Generate fake user registrations and sales for the last 7 days
            for day_offset in range(7, -1, -1):
                date_point = now - timedelta(days=day_offset)
                date_str = date_point.strftime("%Y-%m-%d %H:%M:%S")
                
                # Insert 2-5 users per day
                num_users = random.randint(2, 5)
                for u in range(num_users):
                    user_id = random.randint(10000000, 99999999)
                    username = f"user_{user_id % 1000}"
                    await db.execute(
                        "INSERT INTO users (user_id, username, registered_at) VALUES (?, ?, ?)",
                        (user_id, username, date_str)
                    )
                    
                    # 50% chance they made a purchase
                    if random.random() > 0.5:
                        amount = random.choice([490.0, 990.0, 1490.0, 2490.0])
                        product = random.choice(["TG-Shop-Bot-Source", "Parser-Engine", "Consulting-Hour"])
                        await db.execute(
                            "INSERT INTO sales (user_id, amount, product_name, created_at) VALUES (?, ?, ?, ?)",
                            (user_id, amount, product, date_str)
                        )
            await db.commit()
            print("CRM database populated successfully.")

async def add_user(user_id: int, username: str):
    """Saves user to database if they don't exist yet."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        await db.commit()

async def get_all_users() -> list:
    """Returns list of user IDs for broadcasting newsletters."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]

async def record_sale(user_id: int, amount: float, product_name: str):
    """Logs a sale transaction in database."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO sales (user_id, amount, product_name) VALUES (?, ?, ?)",
            (user_id, amount, product_name)
        )
        await db.commit()

async def get_analytics_data() -> tuple:
    """Retrieves grouped registration and sales volume for the last 7 days."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Group users by date
        user_cursor = await db.execute("""
            SELECT date(registered_at) as reg_date, COUNT(*) 
            FROM users 
            GROUP BY reg_date 
            ORDER BY reg_date DESC 
            LIMIT 7
        """)
        user_rows = await user_cursor.fetchall()
        
        # Group sales revenue by date
        sales_cursor = await db.execute("""
            SELECT date(created_at) as sale_date, SUM(amount) 
            FROM sales 
            GROUP BY sale_date 
            ORDER BY sale_date DESC 
            LIMIT 7
        """)
        sales_rows = await sales_cursor.fetchall()
        
        return user_rows[::-1], sales_rows[::-1]
