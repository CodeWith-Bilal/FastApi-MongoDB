from fastapi import HTTPException, Request
from app.services import user_service
from app.models import user_model 
from app.validations.admin_validations import is_admin

async def create_user(request: Request):
    is_admin(request.state.user)

    data = await request.json()
    user = user_model.UserCreate(**data)

    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        if existing_user.get("is_blocked"):
            raise HTTPException(status_code=403, detail="This user is blocked.")
        raise HTTPException(status_code=400, detail="User with this email already exists")

    return await user_service.create_user(**user.dict())

async def get_all_users(request: Request):
    if not await is_admin(request.state.user["_id"]):
        raise HTTPException(status_code=403, detail="Only admins can view all users")
    return await user_service.get_all_users()

async def delete_user(user_id: str, request: Request):
    if not await is_admin(request.state.user["_id"]):
        raise HTTPException(status_code=403, detail="Only admins can delete users")
    return await user_service.delete_user(user_id)

async def deactivate_user(user_id: str, request: Request):
    if not await is_admin(request.state.user["_id"]):
        raise HTTPException(status_code=403, detail="Only admins can deactivate users")
    return await user_service.deactivate_user(user_id)

async def get_user_by_email(email: str):
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
