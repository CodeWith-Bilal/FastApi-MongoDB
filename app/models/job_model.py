from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

class JobBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    price: float = Field(..., gt=0)
    category: Optional[str] = Field(None, max_length=50)
    status: str = Field("open")
    workplace_type: str
    location: Optional[str] = None
    job_type: str
    experience_level: str
    rate_type: str
    overview: str
    responsibilities: List[str]
    skills_required: List[str]

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: str
    created_by: str
    created_at: datetime
    
    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True