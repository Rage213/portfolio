import asyncio
from scraper import PlaywrightAntiBotScraper

async def main():
    print("=" * 60)
    print("Nexus Labs Anti-Bot Playwright Scraper Engine starting...")
    print("Target: scraping dynamically loaded quotes from quotes.toscrape.com/js/")
    print("=" * 60)
    
    scraper = PlaywrightAntiBotScraper()
    
    try:
        results = await scraper.fetch_dynamic_quotes()
        
        print(f"\nSuccessfully parsed {len(results)} quotes:\n")
        
        for i, quote in enumerate(results):
            print(f"[{i+1}] \"{quote['text']}\"")
            print(f"    — Author: {quote['author']}")
            print(f"    — Tags: {', '.join(quote['tags'])}\n")
            
    except Exception as e:
        print(f"\n❌ Scraper error occurred: {e}")
        print("Tip: If running for the first time, run 'playwright install' in your command prompt to install browser binaries.")

if __name__ == "__main__":
    asyncio.run(main())
