import aiohttp
import re
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PriceParser")

async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    """Asynchronously fetches HTML content from the given URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    async with session.get(url, headers=headers, timeout=10) as response:
        response.raise_for_status()
        return await response.text()

def parse_product_html(html_content: str) -> dict:
    """Parses product name and price from HTML content using Regex.
    Designed to parse books.toscrape.com sandbox pages out of the box.
    """
    result = {"name": None, "price": None}
    
    # 1. Extract product name (typically in h1 tag)
    name_match = re.search(r'<h1>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
    if name_match:
        result["name"] = name_match.group(1).strip()
        
    # 2. Extract price (typically in price_color class tag: £51.77)
    price_match = re.search(r'class="price_color"[^>]*>([^<]+)', html_content, re.IGNORECASE)
    if price_match:
        raw_price = price_match.group(1).strip()
        # Clean price string to isolate float digits (e.g. £51.77 -> 51.77)
        clean_price_match = re.search(r'([\d\.,]+)', raw_price)
        if clean_price_match:
            try:
                result["price"] = float(clean_price_match.group(1).replace(",", "."))
            except ValueError:
                pass
                
    return result

async def scrape_product(session: aiohttp.ClientSession, url: str) -> dict:
    """Asynchronously fetches page and extracts product data."""
    try:
        html = await fetch_page(session, url)
        data = parse_product_html(html)
        if data["name"] and data["price"] is not None:
            return data
        else:
            logger.warning(f"Could not parse name/price from page: {url}")
            return {}
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return {}
