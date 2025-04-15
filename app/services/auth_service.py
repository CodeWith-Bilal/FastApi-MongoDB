from passlib.context import CryptContext
from app.config.db_config import database
from app.models.user_model import user_helper
from datetime import datetime
from fastapi import HTTPException, status
from app.services.user_service import get_user_by_email
from bson import ObjectId
import jwt
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from app.services.user_service import update_user
from datetime import datetime, timedelta
import random
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_collection = database.get_collection("users")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@gmail.com")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Tradala")


async def verify_password(plain_pw: str, hashed_pw: str) -> bool:
    return pwd_context.verify(plain_pw, hashed_pw)
async def get_user_by_id(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(user) if user else None

async def verify_token_and_get_user(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.utcnow().timestamp() > payload.get("exp", 0):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims")

        user = await get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def send_otp_email(email: str, otp: str):
    subject = "Your Password Reset OTP"
    body = f"""
    Your OTP for password reset is: {otp}
    This OTP is valid for 10 minutes.
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = formataddr((EMAIL_FROM_NAME, EMAIL_FROM))
    msg['To'] = email

    try:
        print(f"Sending OTP to: {email}")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USERNAME, SMTP_PASSWORD.strip())
            server.send_message(msg)
            print("Email sent successfully.")
            return True
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(
            status_code=500,
            detail="Email authentication failed. Please check your credentials."
        )
    except Exception as e:
        print(f"SMTP Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Email service temporarily unavailable. Please try again later."
        )
        
async def generate_and_send_otp(email: str) -> str:
    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    if await send_otp_email(email, otp):
        user = await get_user_by_email(email)
        if user:
            await update_user(user["_id"], {
                "otp": otp,
                "otp_expiry": expiry
            })
        return otp
    raise HTTPException(status_code=500, detail="Failed to send OTP email")

