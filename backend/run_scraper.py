import asyncio
import logging

from app.scrapers.rbi import RBIScraper

# Setup basic logging to see the scraper working
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

async def test_scraper():
    print("Initializing LexSentry RBI Scraper...")
    scraper = RBIScraper()
    
    print("Connecting to Reserve Bank of India servers...")
    documents = await scraper.run()
    
    print(f"\nScraper finished! Found {len(documents)} cyber-relevant judgments.")
    
    if documents:
        for idx, doc in enumerate(documents[:3]):
            print(f"\n--- Document {idx + 1} ---")
            print(f"Title: {doc.title}")
            print(f"URL: {doc.original_url}")
            print(f"Snippet: {doc.raw_text[:200]}...")

if __name__ == "__main__":
    asyncio.run(test_scraper())
