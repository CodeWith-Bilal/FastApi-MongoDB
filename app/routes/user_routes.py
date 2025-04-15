from fastapi import APIRouter, Request
from app.controllers import user_controller

router = APIRouter()

@router.post("/")
async def create_user(request: Request):
    return await user_controller.create_user(request)

@router.get("/")
async def get_all_users(request: Request):
    return await user_controller.get_all_users(request)

@router.put("/{user_id}")
async def update_user(user_id: str, request: Request):
    return await user_controller.update_user(user_id, request)

@router.delete("/{user_id}")
async def delete_user(user_id: str, request: Request):
    return await user_controller.delete_user(user_id, request)

@router.post("/{user_id}/block")
async def block_user(user_id: str, request: Request):
    return await user_controller.block_user(user_id, request)

@router.post("/{user_id}/deactivate")
async def deactivate_user(user_id: str, request: Request):
    return await user_controller.deactivate_user(user_id, request)

@router.get("/profile")
async def get_current_user_profile(request: Request):
    return request.state.user
