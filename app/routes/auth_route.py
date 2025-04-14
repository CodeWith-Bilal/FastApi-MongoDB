from fastapi import APIRouter, HTTPException
from app.validations.auth_validations import UserRegister, UserLogin
from app.controllers import auth_controller

router = APIRouter()

@router.post("/register")
async def register(payload: UserRegister):
    user = await auth_controller.register_user(**payload.dict())
    if not user:
        raise HTTPException(status_code=400, detail="User already exists or is blocked")
    return user

@router.post("/login")
async def login(payload: UserLogin):
    user = await auth_controller.login_user(**payload.dict())
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return user
