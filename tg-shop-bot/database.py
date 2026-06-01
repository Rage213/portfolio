import aiosqlite
from config import DB_PATH

async def init_db():
    """Initializes database tables and populates default products if empty."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Create Products table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                image_url TEXT
            )
        ''')
        
        # Create Cart table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                PRIMARY KEY (user_id, product_id),
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        ''')
        
        # Create Orders table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_price REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        await db.commit()
        
        # Populate default products if database is empty
        async with db.execute("SELECT COUNT(*) FROM products") as cursor:
            count = await cursor.fetchone()
            if count and count[0] == 0:
                default_products = [
                    (
                        "🤖 Telegram Bot Scraper", 
                        "Асинхронный бот-парсер, собирающий данные с сайтов объявлений и присылающий уведомления в личку. Полная настройка под ваши источники.", 
                        4500.0, 
                        "https://via.placeholder.com/300x200/5b21b6/ffffff?text=Telegram+Bot+Scraper"
                    ),
                    (
                        "📊 Web Data Parser (Script)", 
                        "Скрипт на Python для сбора цен, товаров, отзывов с любых маркетплейсов. Сохраняет результаты в Excel/CSV/JSON.", 
                        3000.0, 
                        "https://via.placeholder.com/300x200/0369a1/ffffff?text=Data+Parser+Script"
                    ),
                    (
                        "💳 Crypto Payment Gateway", 
                        "Готовый модуль интеграции оплаты криптовалютой (CryptoBot API, Tonkeeper, Lava Pay) для ваших скриптов и ботов.", 
                        3500.0, 
                        "https://via.placeholder.com/300x200/0f766e/ffffff?text=Crypto+Gateway"
                    ),
                    (
                        "🚀 Premium Glassmorphism Landing", 
                        "Современный адаптивный одностраничный сайт в стиле киберпанк/глассморфизм с анимациями и интерактивным ИИ-ассистентом.", 
                        8000.0, 
                        "https://via.placeholder.com/300x200/4d7c0f/ffffff?text=Premium+Landing"
                    )
                ]
                await db.executemany(
                    "INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)",
                    default_products
                )
                await db.commit()
                print("Default database products populated successfully.")

# Product helper functions
async def get_all_products():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM products") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_product_by_id(product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM products WHERE id = ?", (product_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def add_product(name: str, description: str, price: float, image_url: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)",
            (name, description, price, image_url)
        )
        await db.commit()

async def delete_product(product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        await db.commit()

# Cart helper functions
async def add_to_cart(user_id: int, product_id: int, quantity: int = 1):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO cart (user_id, product_id, quantity) 
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, product_id) 
            DO UPDATE SET quantity = quantity + EXCLUDED.quantity
        ''', (user_id, product_id, quantity))
        await db.commit()

async def get_cart(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        query = '''
            SELECT c.product_id, c.quantity, p.name, p.price, p.description 
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
        '''
        async with db.execute(query, (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def update_cart_item_qty(user_id: int, product_id: int, quantity: int):
    async with aiosqlite.connect(DB_PATH) as db:
        if quantity <= 0:
            await db.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
        else:
            await db.execute("UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?", (quantity, user_id, product_id))
        await db.commit()

async def remove_from_cart(user_id: int, product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
        await db.commit()

async def clear_cart(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        await db.commit()

# Order helper functions
async def create_order(user_id: int, total_price: float):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "INSERT INTO orders (user_id, total_price) VALUES (?, ?)",
            (user_id, total_price)
        ) as cursor:
            order_id = cursor.lastrowid
            await db.commit()
            return order_id
