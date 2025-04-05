from typing import Optional

def user_helper(user) -> dict:
    return {
        "id": str(user.get("_id")),
        "email": user.get("email")
    }
