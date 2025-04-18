from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class JobApplicationBase(BaseModel):
    job_id: str
    user_id: str
    cover_letter: str
    proposed_amount: Optional[float] = None
    status: str = "pending" 

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationResponse(JobApplicationBase):
    id: str
    created_at: datetime
    updated_at: datetime


class JobFavorite(BaseModel):
    job_id: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class JobFavoriteResponse(JobFavorite):
    id: str
    owner_id: str  # Add this field to track who favorited the job