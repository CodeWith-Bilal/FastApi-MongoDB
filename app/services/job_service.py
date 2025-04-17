from app.config.db_config import database
from app.models import job_model
from bson import ObjectId
from app.services import job_seeker_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
jobs = database.get_collection("jobs")

def serialize_job(job) -> dict:
    return {
        "id": str(job["_id"]),
        "title": job["title"],
        "description": job["description"],
        "amount": job["amount"],
        "created_by": job["created_by"],
        "created_at": job["created_at"],
        "status": job["status"],
        "category": job.get("category"),
        "workplace_type": job.get("workplace_type"),
        "location": job.get("location"),
        "deadline": job.get("deadline"),
        "min_amount": job.get("min_amount"),
        "max_amount": job.get("max_amount"),
        "preferences": job.get("preferences"),
        "job_type": job.get("job_type"),
        "experience_level": job.get("experience_level"),
        "rate_type": job.get("rate_type"),
        "overview": job.get("overview"),
        "responsibilities": job.get("responsibilities"),
        "skills_required": job.get("skills_required"),
    }

async def create_job(data: dict, user_id: str):
    job = job_model.JobCreate(**data)
    job_data = job.model_dump(exclude_unset=True)
    job_data.update({
        "_id": ObjectId(),
        "created_by": user_id,
        "created_at": datetime.utcnow(),
        "status": "open",
    })
    await jobs.insert_one(job_data)
    return serialize_job(job_data)

async def update_job(job_id: str, data: dict):
    update_model = job_model.JobUpdate(**data)
    update_dict = update_model.model_dump(exclude_unset=True)
    await jobs.update_one({"_id": ObjectId(job_id)}, {"$set": update_dict})
    updated = await jobs.find_one({"_id": ObjectId(job_id)})
    return serialize_job(updated) if updated else None

async def get_all_jobs():
    return [serialize_job(job) async for job in jobs.find()]

async def get_job_by_id(job_id: str):
    job = await jobs.find_one({"_id": ObjectId(job_id)})
    if job:
        job = serialize_job(job)
        job['application_count'] = await job_seeker_service.get_application_count(job_id)
        return job
    return None

async def get_jobs_by_user(user_id: str):
    return [serialize_job(job) async for job in jobs.find({"created_by": user_id})]

async def delete_job(job_id: str):
    result = await jobs.delete_one({"_id": ObjectId(job_id)})
    return {"deleted": result.deleted_count == 1}
