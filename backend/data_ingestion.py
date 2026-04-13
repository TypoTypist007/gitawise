import asyncio
import requests
import logging
from langchain_openai import OpenAIEmbeddings
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_verses():
    logger.info("Fetching Bhagavad Gita verses...")
    try:
        response = requests.get("https://api.bhagavadgita.io/v2/verses")
        return response.json()
    except Exception as e:
        logger.error(f"Error: {e}")
        return []

async def run_ingestion():
    logger.info("Starting data ingestion...")
    verses = await fetch_verses()
    logger.info(f"Fetched {len(verses)} verses")
    return True

if __name__ == "__main__":
    success = asyncio.run(run_ingestion())
    exit(0 if success else 1)
