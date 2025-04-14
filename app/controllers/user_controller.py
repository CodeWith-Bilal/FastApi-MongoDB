from fastapi import HTTPException, status, Request
from app.services import user_service
from app.models.user_model import UserCreate, UserUpdate , PasswordChange
from app.validations.admin_validations import is_admin

async def create_user(request: Request):
    is_admin(request.state.user)

    data = await request.json()
    user = UserCreate(**data)

    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        if existing_user.get("is_blocked"):
            raise HTTPException(status_code=403, detail="This user is blocked.")
        raise HTTPException(status_code=400, detail="User with this email already exists")

    return await user_service.create_user(**user.dict())

async def get_all_users(request: Request):
    is_admin(request.state.user)
    return await user_service.get_all_users()

async def update_user(user_id: str, request: Request):
    current_user = request.state.user

    try:
        is_admin(current_user)
    except HTTPException:
        if str(current_user["_id"]) != user_id:
            raise HTTPException(status_code=403, detail="You can only update your own profile")

    if not await user_service.get_user_by_id(user_id):
        raise HTTPException(status_code=404, detail="User not found")

    data = await request.json()
    user_update = UserUpdate(**data)

    return await user_service.update_user(user_id, user_update.dict(exclude_unset=True))

async def change_password(request: Request):
    user = request.state.user
    data = await request.json()
    password_data = PasswordChange(**data)

    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(status_code=400, detail="New password and confirm password do not match")

    db_user = await user_service.get_user_by_id(str(user["_id"]))
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    from app.services.user_service import pwd_context
    if not pwd_context.verify(password_data.current_password, db_user["password"]):
        raise HTTPException(status_code=403, detail="Incorrect current password")

    hashed_pw = pwd_context.hash(password_data.new_password)
    await user_service.update_user(str(user["_id"]), {"password": hashed_pw})
    return {"message": "Password changed successfully"}


async def delete_user(user_id: str, request: Request):
    is_admin(request.state.user)
    return await user_service.delete_user(user_id)

async def block_user(user_id: str, request: Request):
    is_admin(request.state.user)
    return await user_service.block_user(user_id)

async def deactivate_user(user_id: str, request: Request):
    is_admin(request.state.user)
    return await user_service.deactivate_user(user_id)

async def get_user_by_email(email: str):
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
