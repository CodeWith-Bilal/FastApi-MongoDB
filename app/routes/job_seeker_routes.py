from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from app.controllers import job_seeker_controller
from app.services.job_seeker_service import get_user_id, serialize_doc
router = APIRouter()

@router.post("/apply/{job_id}")
async def apply_for_job(job_id: str, request: Request):
    body = await request.json()
    result = await job_seeker_controller.apply_for_job(job_id, get_user_id(request), body)
    return jsonable_encoder(serialize_doc(result))

@router.get("/proposals/{job_id}")
async def get_job_applications(job_id: str, request: Request):
    result = await job_seeker_controller.get_job_applications(job_id, get_user_id(request))
    return jsonable_encoder([serialize_doc(app) for app in result])

@router.get("/my-proposals")
async def get_user_applications(request: Request):
    result = await job_seeker_controller.get_user_applications(get_user_id(request))
    return jsonable_encoder([serialize_doc(app) for app in result])

@router.post("/favorites/{job_id}")
async def add_favorite_job(job_id: str, request: Request):
    result = await job_seeker_controller.add_job_to_favorites(job_id, get_user_id(request))
    return jsonable_encoder(serialize_doc(result))

@router.delete("/favorites/{job_id}")
async def remove_favorite_job(job_id: str, request: Request):
    await job_seeker_controller.remove_job_from_favorites(job_id, get_user_id(request))
    return {"message": "Job removed from favorites"}

@router.get("/favorites")
async def get_favorite_jobs(request: Request):
    result = await job_seeker_controller.get_user_favorites(get_user_id(request))
    return jsonable_encoder([serialize_doc(job) for job in result])

@router.put("/proposals/{application_id}")
async def update_proposal(application_id: str, request: Request):
    body = await request.json()
    result = await job_seeker_controller.update_proposal(application_id, get_user_id(request), body)
    return jsonable_encoder(serialize_doc(result))

@router.delete("/proposals/{application_id}")
async def delete_proposal(application_id: str, request: Request):
    await job_seeker_controller.delete_proposal(application_id, get_user_id(request))
    return {"message": "Proposal deleted successfully"}


@router.post("/report/{job_id}")
async def report_job(job_id: str, request: Request):
    body = await request.json()
    result = await job_seeker_controller.report_job(
        job_id,
        get_user_id(request),
        body["reason"]
    )
    return jsonable_encoder(result)

@router.get("/reports/{job_id}")
async def get_job_reports(job_id: str, request: Request):
    result = await job_seeker_controller.get_job_reports(
        job_id,
        get_user_id(request)
    )
    return jsonable_encoder(result)

@router.get("/my-reports")
async def get_my_reports(request: Request):
    result = await job_seeker_controller.get_my_reports(get_user_id(request))
    return jsonable_encoder(result)
