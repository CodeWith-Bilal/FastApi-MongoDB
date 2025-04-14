from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class JobBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, 
                      description="Job title must be between 3-100 characters")
    description: str = Field(..., min_length=10, max_length=1000,
                           description="Detailed job description")
    amount: float = Field(..., gt=0, le=1000000,
                        description="amount must be positive and reasonable")
    category: Optional[str] = Field(None, max_length=50,
                                  pattern="^[a-zA-Z0-9 ]+$",
                                  description="Alphanumeric category name")
    workplace_type: str = Field(..., 
                              pattern="^(remote|onsite|hybrid)$",
                              description="Must be remote, onsite or hybrid")
    location: Optional[str] = Field(None, max_length=100,
                                  pattern="^[a-zA-Z0-9 ,.-]+$")
    job_type: str = Field(...,
                        pattern="^(full-time|part-time|contract|freelance)$",
                        description="Valid job types")
    experience_level: str = Field(...,
                                pattern="^(entry level|intermediate|expert)$")
    rate_type: str = Field(...,
                         pattern="^(hourly|daily|weekly|monthly)$")
    overview: str = Field(..., min_length=20, max_length=500,
                        description="Job summary")
    responsibilities: List[str] = Field(..., min_items=1, max_items=20,
                                      description="List of responsibilities")
    skills_required: List[str] = Field(..., min_items=1, max_items=20,
                                    description="Required skills")
    location: Optional[dict] = Field(
        None,
        description="Google Map coordinates in format {'lat': float, 'lng': float}"
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Job application deadline date and time"
    )
    min_amount: Optional[float] = Field(
        None, 
        gt=0,
        description="Minimum acceptable amount for this job"
    )
    max_amount: Optional[float] = Field(
        None,
        gt=0,
        description="Maximum acceptable amount for this job"
    )
    preferences: Optional[dict] = Field(
        None,
        description="Job preference settings"
    )
class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: str
    created_by: str
    created_at: datetime
    status: str = Field("open", description="Job status (open, in_progress, completed)")
    
    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None)
    workplace_type: Optional[str] = Field(None)
    location: Optional[dict] = Field(None)
    job_type: Optional[str] = Field(None)
    experience_level: Optional[str] = Field(None)
    rate_type: Optional[str] = Field(None)
    overview: Optional[str] = Field(None, min_length=20)
    responsibilities: Optional[List[str]] = Field(None, min_items=1)
    skills_required: Optional[List[str]] = Field(None, min_items=1)