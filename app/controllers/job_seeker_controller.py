from fastapi import HTTPException
from app.services import job_service, job_seeker_service

async def apply_for_job(job_id: str, user_id: str, application_data: dict):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    existing_apps = await job_seeker_service.get_user_applications(user_id)
    if any(app["job_id"] == job_id for app in existing_apps):
        raise HTTPException(status_code=400, detail="You have already applied for this job")
    
    return await job_seeker_service.apply_for_job(job_id, user_id, application_data)

async def get_job_applications(job_id: str, user_id: str):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="You can only view applications for your own jobs")
    
    return await job_seeker_service.get_applications_for_job(job_id)

async def get_user_applications(user_id: str):
    return await job_seeker_service.get_user_applications(user_id)


async def add_job_to_favorites(job_id: str, user_id: str):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if await job_seeker_service.is_job_favorited(job_id, user_id):
        raise HTTPException(status_code=400, detail="Job already in favorites")
    
    return await job_seeker_service.add_job_to_favorites(job_id, user_id)

async def remove_job_from_favorites(job_id: str, user_id: str):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    favorite = await job_seeker_service.get_favorite_by_job_and_user(job_id, user_id)
    if not favorite:
        raise HTTPException(
            status_code=403,
            detail="You can only remove jobs you've favorited"
        )
    
    return await job_seeker_service.remove_job_from_favorites(job_id, user_id)

async def get_user_favorites(user_id: str):
    return await job_seeker_service.get_user_favorites(user_id)