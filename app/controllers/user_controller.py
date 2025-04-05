from app.services import user_service
from app.utils.jwt_util import create_jwt_token

async def register_user(email: str, password: str):
    user_exists = await user_service.get_user_by_email(email)
    if user_exists:
        return None
    user = await user_service.create_user(email, password)
    return user

async def login_user(email: str, password: str):
    user = await user_service.get_user_by_email(email)
    if not user:
        return None
    db_user = await user_service.collection.find_one({"email": email})
    if not await user_service.verify_password(password, db_user["password"]):
        return None
    token = create_jwt_token(user["id"])
    return {"access_token": token, "token_type": "bearer"}

