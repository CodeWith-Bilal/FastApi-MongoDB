from typing import Optional

def user_helper(user) -> dict:
    return {
        "id": str(user.get("_id")),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "email": user.get("email")
    }
