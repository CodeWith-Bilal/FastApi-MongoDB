from fastapi import APIRouter, HTTPException
from app.validations.user_validations import UserRegister, UserLogin
from app.controllers import user_controller

router = APIRouter()

@router.post("/register")
async def register(payload: UserRegister):
    user = await user_controller.register_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return user

@router.post("/login")
async def login(payload: UserLogin):
    auth_data = await user_controller.login_user(payload.email, payload.password)
    if not auth_data:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return auth_data
