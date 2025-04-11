from app.config.db_config import database
from app.validations.job_validations import JobCreate, validate_object_id, validate_job_ownership
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)
collection = database.get_collection("jobs")

def serialize_job(job) -> dict:
    return {
        "id": str(job["_id"]),
        "title": job["title"],
        "description": job["description"],
        "price": job["price"],
        "created_by": job["created_by"],
        "created_at": job["created_at"],
        "status": job["status"],
        "category": job.get("category"),
        "workplace_type": job.get("workplace_type"),
        "location": job.get("location"),
        "job_type": job.get("job_type"),
        "experience_level": job.get("experience_level"),
        "rate_type": job.get("rate_type"),
        "overview": job.get("overview"),
        "responsibilities": job.get("responsibilities"),
        "skills_required": job.get("skills_required")
    }

async def create_job(job_data: JobCreate, user_id: str):
    try:
        job_dict = job_data.model_dump(exclude_unset=True)
        job_dict.update({
            "created_by": user_id,
            "created_at": datetime.utcnow(),
            "status": "open"
        })
        result = await collection.insert_one(job_dict)
        created_job = await collection.find_one({"_id": result.inserted_id})
        if not created_job:
            raise HTTPException(status_code=500, detail="Failed to create job")
        return serialize_job(created_job)
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_jobs():
    try:
        jobs = [serialize_job(job) async for job in collection.find()]
        return jobs
    except Exception as e:
        logger.error(f"Error retrieving jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_job_by_id(job_id: str):
    try:
        if not validate_object_id(job_id):
            raise HTTPException(status_code=400, detail="Invalid job ID format")
        job = await collection.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return serialize_job(job)
    except Exception as e:
        logger.error(f"Error retrieving job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_jobs_by_user(user_id: str):
    try:
        jobs = [serialize_job(job) async for job in collection.find({"created_by": user_id})]
        return jobs
    except Exception as e:
        logger.error(f"Error retrieving user jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def update_job(job_id: str, update_data: dict, user_id: str):
    try:
        if not validate_object_id(job_id):
            raise HTTPException(status_code=400, detail="Invalid job ID format")
        job = await collection.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        validate_job_ownership(job, user_id)
        await collection.update_one({"_id": ObjectId(job_id)}, {"$set": update_data})
        updated_job = await collection.find_one({"_id": ObjectId(job_id)})
        return serialize_job(updated_job)
    except Exception as e:
        logger.error(f"Error updating job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def delete_job(job_id: str, user_id: str):
    try:
        if not validate_object_id(job_id):
            raise HTTPException(status_code=400, detail="Invalid job ID format")
        job = await collection.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        validate_job_ownership(job, user_id)
        result = await collection.delete_one({"_id": ObjectId(job_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete job")
        return {"message": "Job deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting job: {e}")
        raise HTTPException(status_code=500, detail=str(e))
