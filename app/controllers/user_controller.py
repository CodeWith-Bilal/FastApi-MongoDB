from fastapi import HTTPException, status
from app.services import user_service
from app.models.user_model import UserCreate, UserUpdate

async def create_user(user: UserCreate, current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create new users"
        )
    
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        if existing_user.get("is_blocked", False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user is blocked and cannot register.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    
    return await user_service.create_user(**user.dict())

async def get_all_users(current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can access all users")
    return await user_service.get_all_users()

async def update_user(user_id: str, user_update: UserUpdate, current_user: dict):
    if current_user.get("role") != "admin" and str(current_user["_id"]) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )
    
    if not await user_service.get_user_by_id(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return await user_service.update_user(user_id, user_update.dict(exclude_unset=True))

async def delete_user(user_id: str, current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete users"
        )
    
    return await user_service.delete_user(user_id)

async def block_user(user_id: str, current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can block users"
        )
    
    return await user_service.block_user(user_id)

async def deactivate_user(user_id: str, current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can deactivate users"
        )
    
    return await user_service.deactivate_user(user_id)

async def get_user_by_email(email: str):
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

