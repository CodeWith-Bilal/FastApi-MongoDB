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
    title: Optional[str] = None
    company: Optional[str] = None
    employment_history: Optional[List[Dict[str, Optional[str]]]] = None
    education_info: Optional[List[Dict[str, Optional[str]]]] = None
    portfolio: Optional[str] = None
    certificates_and_licenses: Optional[List[Dict[str, Optional[str]]]] = None
    languages: Optional[List[Dict[str, Optional[str]]]] = None
    job_preferences: Optional[Dict[str, Optional[str]]] = None

class UserCreate(UserBase):
    password: str

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
    title: Optional[str] = None
    company: Optional[str] = None
    employment_history: Optional[List[Dict[str, Optional[str]]]] = None
    education_info: Optional[List[Dict[str, Optional[str]]]] = None
    portfolio: Optional[str] = None
    certificates_and_licenses: Optional[List[Dict[str, Optional[str]]]] = None
    languages: Optional[List[Dict[str, Optional[str]]]] = None
    job_preferences: Optional[Dict[str, Optional[str]]] = None

class UserResponse(UserBase):
    id: PydanticObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

def user_helper(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "email": user.get("email"),
        "skills": user.get("skills"),
        "description": user.get("description"),
        "address": user.get("address"),
        "phone_number": user.get("phone_number"),
        "gender": user.get("gender"),
        "date_of_birth": user.get("date_of_birth"),
        "title": user.get("title"),
        "company": user.get("company"),
        "employment_history": user.get("employment_history"),
        "education_info": user.get("education_info"),
        "portfolio": user.get("portfolio"),
        "certificates_and_licenses": user.get("certificates_and_licenses"),
        "languages": user.get("languages"),
        "job_preferences": user.get("job_preferences"),
        "password": user.get("password")
    }

