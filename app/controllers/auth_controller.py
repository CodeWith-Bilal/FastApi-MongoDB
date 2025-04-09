from app.services import user_service
from app.utils.jwt_util import create_jwt_token
from app.services.user_service import get_user_by_email
from app.services.auth_service import verify_password

async def register_user(first_name: str, last_name: str, email: str, password: str):
    existing_user = await get_user_by_email(email)
    if existing_user:
        return None
    
    user = await user_service.create_user(first_name, last_name, email, password)
    return {"user": user} 

async def login_user(email: str, password: str):
    user = await user_service.get_user_by_email(email)
    if not user:
        return None
    db_user = await user_service.collection.find_one({"email": email})
    if not await verify_password(password, db_user["password"]):
        return None
    token = create_jwt_token(user["_id"], user["email"])
    return {"user": user, "access_token": token, "token_type": "bearer"}

