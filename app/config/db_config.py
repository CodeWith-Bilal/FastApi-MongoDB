from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "fastapi_auth"

client = AsyncIOMotorClient(MONGO_URI)
database: Database = client[DB_NAME]

