from fastapi import HTTPException, status, Request
from app.services import auth_service, user_service
from app.models.user_model import PasswordChange
from app.services.auth_service import verify_password
from app.utils.jwt_util import create_jwt_token
from app.services.user_service import get_user_by_email
from datetime import datetime

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


async def forgot_password_request(email: str):
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    try:
        otp = await auth_service.generate_and_send_otp(email)
        return {"message": "OTP sent to your email"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def verify_otp(otp: str):
    user = await user_service.get_user_by_otp(otp)
    if not user or datetime.utcnow() > user.get("otp_expiry"):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    await user_service.update_user(
        user["_id"],
        {"otp_verified": True}
    )
    return {"message": "OTP verified successfully"}

async def reset_password(new_password: str, confirm_password: str):
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    user = await user_service.get_user_by_otp_verified()
    if not user:
        raise HTTPException(status_code=403, detail="OTP not verified")

    if datetime.utcnow() > user.get("otp_expiry", datetime.utcnow()):
        await user_service.update_user(
            user["_id"],
            {
                "otp_verified": False,
                "otp": None,
                "otp_expiry": None
            }
        )
        raise HTTPException(status_code=403, detail="OTP verification expired. Please request a new OTP.")

    hashed_password = auth_service.pwd_context.hash(new_password)
    await user_service.update_user(
        user["_id"],
        {
            "password": hashed_password,
            "otp_verified": False,
            "otp": None,
            "otp_expiry": None
        }
    )
    return {"message": "Password updated successfully"}
async def change_password(request: Request):
    user = request.state.user
    data = await request.json()
    password_data = PasswordChange(**data)

    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(status_code=400, detail="New password and confirm password do not match")

    db_user = await auth_service.get_user_by_id(str(user["_id"]))
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not auth_service.pwd_context.verify(password_data.current_password, db_user["password"]):
        raise HTTPException(status_code=403, detail="Incorrect current password")

    hashed_pw = auth_service.pwd_context.hash(password_data.new_password)
    await auth_service.update_user(str(user["_id"]), {"password": hashed_pw})
    return {"message": "Password changed successfully"}
