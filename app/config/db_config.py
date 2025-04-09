from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "fastapi_auth"

client = AsyncIOMotorClient(MONGO_URI)
try:
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print("MongoDB connection error:", e)
    raise

database: Database = client[DB_NAME]
