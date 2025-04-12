from fastapi import APIRouter, Request, status
from typing import List
from app.controllers import user_controller
from app.models.user_model import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, request: Request):
    return await user_controller.create_user(user, request.state.user)

@router.get("/", response_model=List[UserResponse])
async def get_all_users(request: Request):
    return await user_controller.get_all_users(request.state.user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate, request: Request):
    return await user_controller.update_user(user_id, user_update, request.state.user)

@router.delete("/{user_id}")
async def delete_user(user_id: str, request: Request):
    return await user_controller.delete_user(user_id, request.state.user)

@router.post("/{user_id}/block")
async def block_user(user_id: str, request: Request):
    return await user_controller.block_user(user_id, request.state.user)

@router.post("/{user_id}/deactivate")
async def deactivate_user(user_id: str, request: Request):
    return await user_controller.deactivate_user(user_id, request.state.user)

@router.get("/profile", response_model=UserResponse)
async def get_current_user_profile(request: Request):
    return request.state.user
