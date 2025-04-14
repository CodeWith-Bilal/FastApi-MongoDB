from fastapi import APIRouter, Request
from app.controllers import job_controller

router = APIRouter()

@router.post("/")
async def create_job(request: Request):
    body = await request.json()
    return await job_controller.post_job(body, request.state.user["_id"])

@router.get("/all")
async def get_all_jobs():
    return await job_controller.get_all_jobs()

@router.get("/{job_id}")
async def get_job(job_id: str):
    return await job_controller.get_job(job_id)

@router.get("/")
async def get_user_jobs(request: Request):
    return await job_controller.get_user_jobs(request.state.user["_id"])

@router.put("/{job_id}")
async def update_job(job_id: str, request: Request):
    body = await request.json()
    return await job_controller.update_user_job(job_id, body, request.state.user["_id"])

@router.delete("/{job_id}")
async def delete_job(job_id: str, request: Request):
    return await job_controller.delete_user_job(job_id, request.state.user["_id"])
