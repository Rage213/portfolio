import asyncio
import json
import os
import aiohttp
import urllib.parse
import urllib.request
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CHECK_INTERVAL_SECONDS, DB_FILE, TRACKED_PRODUCTS
from parser import scrape_product

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("PriceTracker")

def load_history() -> dict:
    """Loads historical prices from the JSON file database."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading price history: {e}")
    return {}

def save_history(history: dict):
    """Saves price history database to a JSON file."""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving price history: {e}")

async def send_telegram_alert(text: str):
    """Sends HTML formatted message alert to the configured Telegram chat."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram notification settings not configured. Alert printed to console instead:")
        print(f"[TELEGRAM MOCK ALERT]: {text}")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method='POST')
    try:
        # Running sync urlopen in an executor to avoid blocking the async event loop
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, timeout=10).read())
        logger.info("Telegram alert sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send Telegram alert: {e}")

async def track_prices_once(session: aiohttp.ClientSession, history: dict):
    """Performs one scan cycle of all tracked product URLs in parallel."""
    tasks = []
    for item in TRACKED_PRODUCTS:
        tasks.append(scrape_product(session, item["url"]))
        
    # Scrape all items concurrently using asyncio.gather
    results = await asyncio.gather(*tasks)
    
    for item, data in zip(TRACKED_PRODUCTS, results):
        if not data:
            continue
            
        prod_id = item["id"]
        name = data["name"]
        price = data["price"]
        url = item["url"]
        
        prev_price = history.get(prod_id, {}).get("price")
        
        if prev_price is None:
            # First time scanning this item
            logger.info(f"Registered product {name} with price {price} £")
            history[prod_id] = {
                "name": name,
                "price": price,
                "url": url
            }
        elif price < prev_price:
            # Price dropped!
            logger.info(f"Price DROP for {name}: {prev_price} -> {price} £")
            alert_text = (
                f"📉 <b>Снижение цены на товар!</b>\n\n"
                f"📌 <b>{name}</b>\n"
                f"💰 Старая цена: <s>{prev_price} £</s>\n"
                f"🔥 Новая цена: <b>{price} £</b>\n\n"
                f"🔗 <a href='{url}'>Перейти к товару</a>"
            )
            await send_telegram_alert(alert_text)
            
            # Update database record
            history[prod_id]["price"] = price
        elif price > prev_price:
            # Price increased
            logger.info(f"Price INCREASE for {name}: {prev_price} -> {price} £")
            history[prod_id]["price"] = price
        else:
            logger.info(f"No price change for {name}: {price} £")
            
    save_history(history)

async def main():
    logger.info("===============================================")
    logger.info("  🚀 ASYNC PRICE MONITOR & TRACKER STARTING   ")
    logger.info("===============================================")
    
    history = load_history()
    
    # Use single client session for efficient connection pooling
    async with aiohttp.ClientSession() as session:
        while True:
            logger.info("Starting price scanning cycle...")
            await track_prices_once(session, history)
            logger.info(f"Scanning cycle finished. Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Tracker stopped.")
