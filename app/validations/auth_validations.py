from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    first_name: str = Field(..., min_length=1, description="First name is required")
    last_name: str = Field(..., min_length=1, description="Last name is required")
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    confirm_password: str = Field(..., min_length=6, description="Confirm password must match new password")
