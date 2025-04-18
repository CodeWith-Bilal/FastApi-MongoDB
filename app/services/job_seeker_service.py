from app.config.db_config import database
from bson import ObjectId
from datetime import datetime
from app.services import job_service

job_applications = database.get_collection("job_applications")
favorites_collection = database.get_collection("favorites")

async def apply_for_job(job_id: str, user_id: str, application_data: dict):
    application = {
        "job_id": job_id,
        "user_id": user_id,
        "cover_letter": application_data["cover_letter"],
        "proposed_amount": application_data.get("proposed_amount"),
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = await job_applications.insert_one(application)
    application["_id"] = result.inserted_id
    return application

async def get_applications_for_job(job_id: str):
    applications = await job_applications.find({"job_id": job_id}).to_list(None)
    return [serialize_application(app) for app in applications]

async def get_application_count(job_id: str):
    return await job_applications.count_documents({"job_id": job_id})

def serialize_application(app):
    return {
        "id": str(app["_id"]),
        "job_id": app["job_id"],
        "user_id": app["user_id"],
        "cover_letter": app["cover_letter"],
        "proposed_amount": app.get("proposed_amount"),
        "status": app["status"],
        "created_at": app["created_at"],
        "updated_at": app["updated_at"]
    }

async def get_user_applications(user_id: str):
    return [app async for app in job_applications.find({"user_id": user_id})]

async def add_job_to_favorites(job_id: str, user_id: str):
    favorite = {
        "job_id": job_id,
        "user_id": user_id,
        "created_at": datetime.utcnow()
    }
    result = await favorites_collection.insert_one(favorite)
    favorite["_id"] = result.inserted_id
    return favorite

async def remove_job_from_favorites(job_id: str, user_id: str):
    result = await favorites_collection.delete_one({
        "job_id": job_id,
        "user_id": user_id
    })
    return result.deleted_count > 0

async def is_job_favorited(job_id: str, user_id: str):
    return await favorites_collection.count_documents({
        "job_id": job_id,
        "user_id": user_id
    }) > 0

async def get_user_favorites(user_id: str):
    favorites = await favorites_collection.find({"user_id": user_id}).to_list(None)
    jobs = []
    for fav in favorites:
        job = await job_service.get_job_by_id(fav["job_id"])
        if job:
            jobs.append({
                **job,
                "favorite_id": str(fav["_id"]),
                "favorited_at": fav["created_at"]
            })
    return jobs

async def get_favorite_by_job_and_user(job_id: str, user_id: str):
    return await favorites_collection.find_one({
        "job_id": job_id,
        "user_id": user_id
    })