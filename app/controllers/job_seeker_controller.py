from fastapi import HTTPException
from app.services import job_service, job_seeker_service
from app.validations.admin_validations import is_admin
async def apply_for_job(job_id: str, user_id: str, data: dict):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    
    user_apps = await job_seeker_service.get_user_applications(user_id)
    if any(app["job_id"] == job_id for app in user_apps):
        raise HTTPException(400, "You have already applied for this job")

    return await job_seeker_service.apply_for_job(job_id, user_id, data)

async def get_job_applications(job_id: str, user_id: str):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job["created_by"] != user_id:
        raise HTTPException(403, "You can only view applications for your own jobs")
    
    return await job_seeker_service.get_applications_for_job(job_id)

async def get_user_applications(user_id: str):
    return await job_seeker_service.get_user_applications(user_id)

async def update_proposal(application_id: str, user_id: str, data: dict):
    app = await job_seeker_service.get_application_by_id(application_id)
    if not app:
        raise HTTPException(404, "Application not found")
    if app["user_id"] != user_id:
        raise HTTPException(403, "You can only update your own proposals")
    
    return await job_seeker_service.update_proposal(application_id, data)

async def delete_proposal(application_id: str, user_id: str):
    app = await job_seeker_service.get_application_by_id(application_id)
    if not app:
        raise HTTPException(404, "Application not found")
    if app["user_id"] != user_id:
        raise HTTPException(403, "You can only delete your own proposals")

    return await job_seeker_service.delete_proposal(application_id)

async def add_job_to_favorites(job_id: str, user_id: str):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    if await job_seeker_service.is_job_favorited(job_id, user_id):
        raise HTTPException(400, "Job already in favorites")

    return await job_seeker_service.add_job_to_favorites(job_id, user_id)

async def remove_job_from_favorites(job_id: str, user_id: str):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    favorite = await job_seeker_service.get_favorite_by_job_and_user(job_id, user_id)
    if not favorite:
        raise HTTPException(403, "You can only remove jobs you've favorited")

    return await job_seeker_service.remove_job_from_favorites(job_id, user_id)

async def get_user_favorites(user_id: str):
    return await job_seeker_service.get_user_favorites(user_id)


async def report_job(job_id: str, reporter_id: str, reason: str):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    
    return await job_seeker_service.create_job_report(job_id, reporter_id, reason)

async def get_job_reports(job_id: str, user_id: str):
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    
    # Only job owner or admin can view reports
    if job["created_by"] != user_id and not await is_admin(user_id):
        raise HTTPException(403, "Unauthorized access to reports")
    
    return await job_seeker_service.get_reports_for_job(job_id)

async def get_my_reports(user_id: str):
    return await job_seeker_service.get_user_reports(user_id)

async def resolve_report(report_id: str, admin_id: str, notes: str):
    # Verify admin status
    if not await is_admin(admin_id):
        raise HTTPException(403, "Only admins can resolve reports")
    
    # Update report status and add admin notes
    return await job_seeker_service.resolve_report(report_id, notes)

async def get_pending_reports():
    return await job_seeker_service.get_pending_reports()
