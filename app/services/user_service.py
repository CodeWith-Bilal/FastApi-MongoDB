from app.config.db_config import database
from app.models.user_model import user_helper
from passlib.context import CryptContext
from bson import ObjectId
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

collection = database.get_collection("users")

async def get_user_by_email(email: str):
    user = await collection.find_one({"email": email})
    return user_helper(user) if user else None

async def get_all_users():
    users = []
    async for user in collection.find():
        users.append(user_helper(user))
    return users

async def create_user(first_name: str, last_name: str, email: str, password: str):
    hashed_pw = pwd_context.hash(password)
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_pw,
    }
    result = await collection.insert_one(user)
    user["_id"] = result.inserted_id
    return user_helper(user)

async def update_user(user_id: str, update_data: dict, current_user_email: str):
    user = await get_user_by_email(current_user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    result = await collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    updated_user = await collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(updated_user)

async def delete_user(user_id: str, current_user_email: str):
    user = await get_user_by_email(current_user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": "User deleted successfully"}

async def change_password(email: str, old_password: str, new_password: str):
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(old_password, user["password"]):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    hashed_new_pw = pwd_context.hash(new_password)
    result = await collection.update_one(
        {"email": email},
        {"$set": {"password": hashed_new_pw}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Password update failed")

    return {"message": "Password updated successfully"}

