from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.jwt_util import decode_jwt
from app.services import user_service
import logging

logger = logging.getLogger(__name__)

async def auth_middleware(request: Request, call_next):
    if request.url.path in ["/auth/login", "/auth/register", "/docs", "/redoc", "/openapi.json", "/"]:
        return await call_next(request)
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(
            status_code=401,
            content={"detail": "Authorization header missing"}
        )
    
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authentication scheme"}
            )
    except ValueError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid token format"}
        )
    
    try:
        payload = decode_jwt(token)
        if not payload:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )
        
        user_id = payload.get("sub")
        if not user_id:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token payload"}
            )
        
        email = payload.get("email")
        if email:
            user = await user_service.get_user_by_email(email)
        else:
            user = None
            
        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "User not found"}
            )
        
        request.state.user = user
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return JSONResponse(
            status_code=401,
            content={"detail": f"Authentication failed: {str(e)}"}
        )
    
    return await call_next(request)