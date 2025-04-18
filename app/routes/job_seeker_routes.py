from fastapi import APIRouter, Request
from app.controllers import job_seeker_controller
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from typing import List, Dict, Any

router = APIRouter()

def serialize_application(app: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to JSON-serializable format"""
    if '_id' in app:
        app['id'] = str(app['_id'])
        del app['_id']
    if isinstance(app.get('created_by'), ObjectId):
        app['created_by'] = str(app['created_by'])
    return app

@router.post("/apply/{job_id}")
async def apply_for_job(job_id: str, request: Request):
    body = await request.json()
    result = await job_seeker_controller.apply_for_job(
        job_id, 
        str(request.state.user["_id"]),
        body
    )
    return jsonable_encoder(serialize_application(result))

@router.get("/applications/{job_id}")
async def get_job_applications(job_id: str, request: Request):
    result = await job_seeker_controller.get_job_applications(
        job_id,
        str(request.state.user["_id"])
    )
    return jsonable_encoder([serialize_application(app) for app in result])

@router.get("/my-applications")
async def get_user_applications(request: Request):
    result = await job_seeker_controller.get_user_applications(
        str(request.state.user["_id"])
    )
    return jsonable_encoder([serialize_application(app) for app in result])

@router.post("/favorites/{job_id}")
async def add_favorite_job(job_id: str, request: Request):
    result = await job_seeker_controller.add_job_to_favorites(
        job_id,
        str(request.state.user["_id"])
    )
    return jsonable_encoder(serialize_application(result))

@router.delete("/favorites/{job_id}")
async def remove_favorite_job(job_id: str, request: Request):
    result = await job_seeker_controller.remove_job_from_favorites(
        job_id,
        str(request.state.user["_id"])
    )
    return {"message": "Job removed from favorites"}

def serialize_favorite_job(fav_job: Dict[str, Any]) -> Dict[str, Any]:
    """Convert favorite job with full details to JSON-serializable format"""
    fav_job['id'] = fav_job.get('id', str(fav_job.get('_id', '')))
    if '_id' in fav_job:
        del fav_job['_id']
    if isinstance(fav_job.get('created_by'), ObjectId):
        fav_job['created_by'] = str(fav_job['created_by'])
    return fav_job

@router.get("/favorites")
async def get_favorite_jobs(request: Request):
    result = await job_seeker_controller.get_user_favorites(
        str(request.state.user["_id"])
    )
    return jsonable_encoder([serialize_favorite_job(job) for job in result])