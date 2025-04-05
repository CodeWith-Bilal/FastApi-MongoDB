from app.config.db_config import database
from app.models.user_model import user_helper
from passlib.context import CryptContext
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

collection = database.get_collection("users")

async def get_user_by_email(email: str):
    user = await collection.find_one({"email": email})
    return user_helper(user) if user else None

async def create_user(email: str, password: str):
    hashed_pw = pwd_context.hash(password)
    user = {"email": email, "password": hashed_pw}
    result = await collection.insert_one(user)
    user["_id"] = result.inserted_id
    return user_helper(user)

async def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)