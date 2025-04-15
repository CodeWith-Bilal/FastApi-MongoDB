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
    user_update = user_model.UserUpdate(**data)

    return await user_service.update_user(user_id, user_update.dict(exclude_unset=True))

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
