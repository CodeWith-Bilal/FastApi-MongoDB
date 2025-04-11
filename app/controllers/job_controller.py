from fastapi import HTTPException, status
from app.services.job_service import create_job, get_job_by_id, get_jobs_by_user, update_job, delete_job, get_all_jobs as service_get_all_jobs
from app.validations.job_validations import JobCreate, JobResponse, JobUpdate, validate_object_id

async def post_job(job_data: JobCreate, user_id: str):
    return await create_job(job_data, user_id)

async def get_job(job_id: str):
    if not validate_object_id(job_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format"
        )
    return await get_job_by_id(job_id)

async def get_user_jobs(user_id: str):
    return await get_jobs_by_user(user_id)

async def get_all_jobs():
    return await service_get_all_jobs()

async def update_user_job(job_id: str, update_data: JobUpdate, user_id: str):
    if not validate_object_id(job_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format"
        )
    
    update_dict = update_data.model_dump(exclude_unset=True)
    return await update_job(job_id, update_dict, user_id)

async def delete_user_job(job_id: str, user_id: str):
    if not validate_object_id(job_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format"
        )
    return await delete_job(job_id, user_id)