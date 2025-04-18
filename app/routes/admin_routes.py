from fastapi import APIRouter, Request
from app.controllers import job_seeker_controller
from app.services.job_seeker_service import get_user_id
from app.controllers import job_controller
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.put("/reports/{report_id}/resolve")
async def resolve_report(report_id: str, request: Request):
    body = await request.json()
    result = await job_seeker_controller.resolve_report(
        report_id,
        get_user_id(request),
        body["notes"]
    )
    return jsonable_encoder(result)

@router.get("/reports/pending")
async def get_pending_reports(request: Request):
    result = await job_seeker_controller.get_pending_reports()
    return jsonable_encoder(result)

@router.put("/jobs/{job_id}/block")
async def block_job(job_id: str, request: Request):
    result = await job_controller.block_job(
        job_id,
        str(request.state.user["_id"])
    )
    return jsonable_encoder(result)

@router.put("/jobs/{job_id}/unblock")
async def unblock_job(job_id: str, request: Request):
    result = await job_controller.unblock_job(
        job_id,
        str(request.state.user["_id"])
    )
    return jsonable_encoder(result)