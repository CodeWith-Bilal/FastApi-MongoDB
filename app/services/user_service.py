from app.config.db_config import database
from app.models.user_model import user_helper
from passlib.context import CryptContext
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_collection = database.get_collection("users")

async def get_user_by_email(email: str):
    user = await user_collection.find_one({"email": email})
    return user_helper(user) if user else None

async def get_user_by_id(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(user) if user else None

async def get_all_users():
    return [user_helper(user) async for user in user_collection.find()]

async def create_user(first_name: str, last_name: str, email: str, password: str, **kwargs):
    hashed_pw = pwd_context.hash(password)
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_pw,
        "role": kwargs.get("role", "user"),
        "active": kwargs.get("active", True),
        **kwargs
    }
    result = await user_collection.insert_one(user)
    user["_id"] = result.inserted_id
    return user_helper(user)

async def deactivate_user(user_id: str):
    await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"active": False}}
    )
    return {"message": "User deactivated successfully"}

async def update_user(user_id: str, update_data: dict):
    update_data.pop("_id", None)
    await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    updated_user = await user_collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(updated_user) if updated_user else None

async def delete_user(user_id: str):
    await user_collection.delete_one({"_id": ObjectId(user_id)})
    return {"message": "User deleted successfully"}
async def block_user(user_id: str):
    await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_blocked": True}}
    )
    return {"message": "User blocked successfully"}

async def get_user_by_otp(otp: str):
    return await user_collection.find_one({"otp": otp})

async def get_user_by_otp_verified():
    return await user_collection.find_one({"otp_verified": True})
