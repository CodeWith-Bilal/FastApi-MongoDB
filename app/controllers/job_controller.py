from fastapi import HTTPException
from app.services import job_service
from app.validations import job_validations
from app.validations.admin_validations import is_admin
from app.services import job_seeker_service

async def post_job(job_data: dict, user_id: str):
    try:
        job_validations.validate_job_data(job_data)
        return await job_service.create_job(job_data, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def update_user_job(job_id: str, update_data: dict, user_id: str):
    if not job_validations.validate_object_id(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_validations.validate_job_ownership(job, user_id)
    
    if await job_seeker_service.get_application_count(job_id) > 0:
        raise HTTPException(status_code=400, detail="Cannot update job that has applications")
    
    if update_data:
        job_validations.validate_job_data({
            k: v for k, v in update_data.items() if k in job_validations.required_fields
        })
    
    return await job_service.update_job(job_id, update_data)

async def delete_user_job(job_id: str, user_id: str):
    if not job_validations.validate_object_id(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_validations.validate_job_ownership(job, user_id)
    
    if await job_seeker_service.get_application_count(job_id) > 0:
        raise HTTPException(status_code=400, detail="Cannot delete job that has applications"
        )
    
    result = await job_service.delete_job(job_id)
    if not result.get("deleted"):
        raise HTTPException(status_code=500, detail="Failed to delete job")
    return {"message": "Job deleted successfully"}

async def get_job(job_id: str, user_id: str = None):
    if not job_validations.validate_object_id(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    job = await job_service.get_job_by_id(job_id, user_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

async def get_all_jobs(user_id: str = None):
    return await job_service.get_all_jobs(user_id)

async def get_user_jobs(user_id: str):
    # Show all jobs (including blocked) to owner
    return await job_service.get_jobs_by_user(user_id)

async def get_job_applications(job_id: str, user_id: str):
    if not job_validations.validate_object_id(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_validations.validate_job_ownership(job, user_id)
    
    return await job_seeker_service.get_applications_for_job(job_id)

async def block_job(job_id: str, admin_id: str):
    if not job_validations.validate_object_id(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    
    # Verify admin status using user_id
    if not await is_admin(admin_id):
        raise HTTPException(status_code=403, detail="Only admins can block jobs")
    
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return await job_service.update_job(job_id, {"status": "blocked"})

async def unblock_job(job_id: str, admin_id: str):
    if not job_validations.validate_object_id(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID format")
    
    if not await is_admin(admin_id):
        raise HTTPException(status_code=403, detail="Only admins can unblock jobs")
    
    # Pass admin_check=True to bypass status filter
    job = await job_service.get_job_by_id(job_id, admin_id, admin_check=True)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return await job_service.update_job(job_id, {"status": "active"})
