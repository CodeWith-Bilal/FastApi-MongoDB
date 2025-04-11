from fastapi import APIRouter, Request, HTTPException, status, Depends
from app.controllers.job_controller import post_job, get_job, get_user_jobs, update_user_job, delete_user_job, get_all_jobs
from app.validations.job_validations import JobCreate, JobResponse, JobUpdate
from typing import List, Dict

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={
        404: {"description": "Job not found"},
        400: {"description": "Bad request - Invalid input"},
        401: {"description": "Unauthorized - Authentication required"},
        403: {"description": "Forbidden - Insufficient permissions"}
    },
)

@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED, 
             summary="Create a new job", 
             description="Create a new job posting. Requires authentication.")
async def create_job(job: JobCreate, request: Request):
    current_user = request.state.user
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await post_job(job, current_user["_id"])

@router.get("/all", response_model=List[JobResponse],
            summary="Get all jobs",
            description="Get all jobs in the system. No authentication required.")
async def read_all_jobs():
    return await get_all_jobs()

@router.get("/{job_id}", response_model=JobResponse,
            summary="Get job by ID",
            description="Get a specific job by its ID. No authentication required.")
async def read_job(job_id: str):
    return await get_job(job_id)

@router.get("", response_model=List[JobResponse],
            summary="Get user's jobs",
            description="Get all jobs created by the authenticated user. Requires authentication.")
async def read_user_jobs(request: Request):
    current_user = request.state.user
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await get_user_jobs(current_user["_id"])

@router.put("/{job_id}", response_model=JobResponse,
            summary="Update job",
            description="Update a job. Only the job creator can update it. Requires authentication.")
async def update_job(job_id: str, job_update: JobUpdate, request: Request):
    current_user = request.state.user
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await update_user_job(job_id, job_update, current_user["_id"])

@router.delete("/{job_id}", response_model=Dict[str, str],
               summary="Delete job",
               description="Delete a job. Only the job creator can delete it. Requires authentication.")
async def delete_job(job_id: str, request: Request):
    current_user = request.state.user
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return await delete_user_job(job_id, current_user["_id"])