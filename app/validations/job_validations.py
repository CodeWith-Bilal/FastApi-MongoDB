from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status

class JobBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Job title must be between 3-100 characters")
    description: str = Field(..., min_length=10, description="Description must be at least 10 characters")
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    category: Optional[str] = Field(None, max_length=50, description="Optional job category")
    workplace_type: str = Field(..., description="Type of workplace (remote, onsite, hybrid)")
    location: Optional[str] = Field(None, description="Job location, required for onsite and hybrid jobs")
    job_type: str = Field(..., description="Job type (full-time, part-time, contract, freelance)")
    experience_level: str = Field(..., description="Required experience level (entry level, intermediate, expert)")
    rate_type: str = Field(..., description="Payment rate type (hourly, daily, weekly, monthly)")
    overview: str = Field(..., min_length=20, description="Brief overview of the job")
    responsibilities: List[str] = Field(..., min_items=1, description="List of job responsibilities")
    skills_required: List[str] = Field(..., min_items=1, description="List of required skills")

class JobCreate(JobBase):
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if len(v) < 3 or len(v) > 100:
            raise ValueError('Title must be between 3 and 100 characters')
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if len(v) < 10:
            raise ValueError('Description must be at least 10 characters')
        return v
    
    @field_validator('workplace_type')
    @classmethod
    def validate_workplace_type(cls, v):
        valid_types = ["remote", "onsite", "hybrid"]
        if v not in valid_types:
            raise ValueError(f'Workplace type must be one of: {", ".join(valid_types)}')
        return v
    
    @field_validator('location')
    @classmethod
    def validate_location(cls, v, info):
        workplace_type = info.data.get('workplace_type')
        if workplace_type in ['onsite', 'hybrid'] and not v:
            raise ValueError('Location is required for onsite and hybrid jobs')
        return v
    
    @field_validator('job_type')
    @classmethod
    def validate_job_type(cls, v):
        valid_types = ["full-time", "part-time", "contract", "freelance"]
        if v not in valid_types:
            raise ValueError(f'Job type must be one of: {", ".join(valid_types)}')
        return v
    
    @field_validator('experience_level')
    @classmethod
    def validate_experience_level(cls, v):
        valid_levels = ["entry level", "intermediate", "expert"]
        if v not in valid_levels:
            raise ValueError(f'Experience level must be one of: {", ".join(valid_levels)}')
        return v
    
    @field_validator('rate_type')
    @classmethod
    def validate_rate_type(cls, v):
        valid_types = ["hourly", "daily", "weekly", "monthly"]
        if v not in valid_types:
            raise ValueError(f'Rate type must be one of: {", ".join(valid_types)}')
        return v
    
    @field_validator('responsibilities')
    @classmethod
    def validate_responsibilities(cls, v):
        if not v or len(v) < 1:
            raise ValueError('At least one responsibility must be provided')
        return v
    
    @field_validator('skills_required')
    @classmethod
    def validate_skills_required(cls, v):
        if not v or len(v) < 1:
            raise ValueError('At least one required skill must be provided')
        return v

class JobResponse(JobBase):
    id: str
    created_by: str
    created_at: datetime
    status: str = Field("open", description="Job status (open, in_progress, completed)")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }
        
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = ["open", "in_progress", "completed"]
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
        
class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="Job title must be between 3-100 characters")
    description: Optional[str] = Field(None, min_length=10, description="Description must be at least 10 characters")
    price: Optional[float] = Field(None, gt=0, description="Price must be greater than 0")
    category: Optional[str] = Field(None, max_length=50, description="Optional job category")
    status: Optional[str] = Field(None, description="Job status (open, in_progress, completed)")
    workplace_type: Optional[str] = Field(None, description="Type of workplace (remote, onsite, hybrid)")
    location: Optional[str] = Field(None, description="Job location, required for onsite and hybrid jobs")
    job_type: Optional[str] = Field(None, description="Job type (full-time, part-time, contract, freelance)")
    experience_level: Optional[str] = Field(None, description="Required experience level (entry level, intermediate, expert)")
    rate_type: Optional[str] = Field(None, description="Payment rate type (hourly, daily, weekly, monthly)")
    overview: Optional[str] = Field(None, min_length=20, description="Brief overview of the job")
    responsibilities: Optional[List[str]] = Field(None, min_items=1, description="List of job responsibilities")
    skills_required: Optional[List[str]] = Field(None, min_items=1, description="List of required skills")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["open", "in_progress", "completed"]
            if v not in valid_statuses:
                raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be greater than 0')
        return v
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if v is not None and (len(v) < 3 or len(v) > 100):
            raise ValueError('Title must be between 3 and 100 characters')
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v is not None and len(v) < 10:
            raise ValueError('Description must be at least 10 characters')
        return v
    
    @field_validator('workplace_type')
    @classmethod
    def validate_workplace_type(cls, v):
        if v is not None:
            valid_types = ["remote", "onsite", "hybrid"]
            if v not in valid_types:
                raise ValueError(f'Workplace type must be one of: {", ".join(valid_types)}')
        return v
    
    @field_validator('job_type')
    @classmethod
    def validate_job_type(cls, v):
        if v is not None:
            valid_types = ["full-time", "part-time", "contract", "freelance"]
            if v not in valid_types:
                raise ValueError(f'Job type must be one of: {", ".join(valid_types)}')
        return v
    
    @field_validator('experience_level')
    @classmethod
    def validate_experience_level(cls, v):
        if v is not None:
            valid_levels = ["entry level", "intermediate", "expert"]
            if v not in valid_levels:
                raise ValueError(f'Experience level must be one of: {", ".join(valid_levels)}')
        return v
    
    @field_validator('rate_type')
    @classmethod
    def validate_rate_type(cls, v):
        if v is not None:
            valid_types = ["hourly", "daily", "weekly", "monthly"]
            if v not in valid_types:
                raise ValueError(f'Rate type must be one of: {", ".join(valid_types)}')
        return v

def validate_object_id(id_str: str) -> bool:
    "Validate if a string is a valid MongoDB ObjectId"
    return ObjectId.is_valid(id_str)

def validate_job_ownership(job: Dict[str, Any], user_id: str) -> None:
    "Validate if a job belongs to a user"
    if job["created_by"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this job"
        )