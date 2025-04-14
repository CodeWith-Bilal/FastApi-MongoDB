from fastapi import HTTPException, status
from app.services import user_service
from app.services.auth_service import verify_password
from app.utils.jwt_util import create_jwt_token
from app.services.user_service import get_user_by_email

async def register_user(first_name: str, last_name: str, email: str, password: str):
    existing_user = await get_user_by_email(email)
    
    if existing_user:
        if existing_user.get("is_blocked") or not existing_user.get("active", True):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user cannot register.")
        return None

    user = await user_service.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role="user",
        active=True
    )
    return {"user": user}

async def login_user(email: str, password: str):
    user = await get_user_by_email(email)

    if not user or not user.get("active", True):
        return None

    if not await verify_password(password, user["password"]):
        return None

    token = create_jwt_token(user["_id"], user["email"])
    return {
        "user": user,
        "access_token": token,
        "token_type": "bearer"
    }
