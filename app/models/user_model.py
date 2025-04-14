from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Annotated, List, Dict
from bson import ObjectId
from datetime import datetime

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator, _field_schema):
        return {"type": "string"}

PydanticObjectId = Annotated[str, PyObjectId]

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    skills: Optional[List[str]] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    employment_history: Optional[List[Dict[str, Optional[str]]]] = None
    education_info: Optional[List[Dict[str, Optional[str]]]] = None
    portfolio: Optional[str] = None
    certificates_and_licenses: Optional[List[Dict[str, Optional[str]]]] = None
    languages: Optional[List[Dict[str, Optional[str]]]] = None
    job_preferences: Optional[Dict[str, Optional[str]]] = None
    role: Optional[str] = "user"
    active: Optional[bool] = True 
    is_blocked: Optional[bool] = False


class UserCreate(UserBase):
    password: str
    active: Optional[bool] = True 
    
class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
    
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    skills: Optional[List[str]] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    employment_history: Optional[List[Dict[str, Optional[str]]]] = None
    education_info: Optional[List[Dict[str, Optional[str]]]] = None
    portfolio: Optional[str] = None
    certificates_and_licenses: Optional[List[Dict[str, Optional[str]]]] = None
    languages: Optional[List[Dict[str, Optional[str]]]] = None
    job_preferences: Optional[Dict[str, Optional[str]]] = None

class UserResponse(UserBase):
    id: PydanticObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})

def user_helper(user) -> dict:
    return {
        "_id": str(user["_id"]),
        **{k: user.get(k) for k in UserBase.__fields__.keys()},
        "password": user.get("password"),
        "is_blocked": user.get("is_blocked", False) 
    }