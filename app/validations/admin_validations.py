from app.services import user_service

async def is_admin(user_id: str) -> bool:
    user = await user_service.get_user_by_id(user_id)
    return user and user.get("role") == "admin"
