from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
snippets_collection = db.code_snippets
comments_collection = db.comments
ads_config_collection = db.google_ads_config
subscribers_collection = db.subscribers

async def get_db():
    """Get database instance"""
    return db

async def close_db_connection():
    client.close()