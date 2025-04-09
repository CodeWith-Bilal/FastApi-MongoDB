from fastapi import APIRouter, Request, HTTPException, status
from app.controllers import user_controller
from app.models.user_model import UserCreate, UserUpdate, UserResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    "Create a new user"
    return await user_controller.create_user(user)

@router.get("/", response_model=List[UserResponse])
async def get_all_users():
    "Get all users Only authenticated users can access this endpoint"
    return await user_controller.get_all_users()

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate, request: Request):
    "Update a user Only the authenticated user can update their own profile"
    current_user = request.state.user
    return await user_controller.update_user(user_id, user_update, current_user["email"])

@router.delete("/{user_id}")
async def delete_user(user_id: str, request: Request):
    "Delete a user Only the authenticated user can delete their own profile"
    current_user = request.state.user
    return await user_controller.delete_user(user_id, current_user["email"])

@router.get("/profile", response_model=UserResponse)
async def get_current_user_profile(request: Request):
    "Get current user profile"
    current_user = request.state.user
    return current_user