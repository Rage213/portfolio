import os
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Load configurations
load_dotenv()
HEADLESS = os.getenv("HEADLESS_MODE", "True").lower() == "true"

class PlaywrightAntiBotScraper:
    """
    Asynchronous web scraper using Playwright to handle JavaScript-heavy sites
    and simulate realistic human-like browsing configurations.
    """
    
    def __init__(self):
        self.target_url = "http://quotes.toscrape.com/js/"
        # Human-like browser configuration
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.viewport = {"width": 1280, "height": 720}

    async def fetch_dynamic_quotes(self) -> list:
        """
        Launches Playwright headless browser, sets headers, bypasses JS checks,
        waits for rendering, and parses quotes list.
        """
        quotes_data = []
        
        async with async_playwright() as p:
            print("Launching Chromium browser...")
            browser = await p.chromium.launch(headless=HEADLESS)
            
            # Setup context with realistic User-Agent and viewport dimensions
            context = await browser.new_context(
                user_agent=self.user_agent,
                viewport=self.viewport,
                locale="ru-RU",
                timezone_id="Europe/Moscow"
            )
            
            page = await context.new_page()
            
            # Bypassing simple webdriver detection flags
            await page.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            print(f"Navigating to: {self.target_url}")
            # Load page and wait until network is idle
            await page.goto(self.target_url, wait_until="networkidle")
            
            # Wait for dynamic JS content to render
            print("Waiting for dynamic selector to render...")
            await page.wait_for_selector(".quote")
            
            # Get rendered HTML source code
            html_content = await page.content()
            await browser.close()
            print("Browser closed. Parsing content...")
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            quotes = soup.select(".quote")
            
            for item in quotes:
                text_el = item.select_one(".text")
                author_el = item.select_one(".author")
                tags_el = item.select(".tag")
                
                text = text_el.text.strip() if text_el else ""
                author = author_el.text.strip() if author_el else ""
                tags = [t.text.strip() for t in tags_el]
                
                quotes_data.append({
                    "text": text,
                    "author": author,
                    "tags": tags
                })
                
        return quotes_data
