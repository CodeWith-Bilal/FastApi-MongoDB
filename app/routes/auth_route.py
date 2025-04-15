from fastapi import APIRouter, HTTPException, Body ,Request
from app.validations import auth_validations
from app.controllers import auth_controller

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/register")
async def register(payload: auth_validations.UserRegister):
    user = await auth_controller.register_user(**payload.dict())
    if not user:
        raise HTTPException(status_code=400, detail="User already exists or is blocked")
    return user

@router.post("/login")
async def login(payload: auth_validations.UserLogin):
    user = await auth_controller.login_user(**payload.dict())
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return user

@router.put("/change-password")
async def change_password(request: Request):
    return await auth_controller.change_password(request)


@router.post("/forgot-password")
async def forgot_password(payload: auth_validations.ForgotPasswordRequest):
    return await auth_controller.forgot_password_request(payload.email)


@router.post("/verify-otp")
async def verify_otp_route(otp: str = Body(..., embed=True)):
    return await auth_controller.verify_otp(otp)

@router.post("/reset-password")
async def reset_password(payload: auth_validations.ResetPasswordRequest):
    return await auth_controller.reset_password(
        payload.new_password,
        payload.confirm_password
    )
