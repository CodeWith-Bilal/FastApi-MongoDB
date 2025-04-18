from fastapi import Request
from typing import Dict, Any
from app.config.db_config import database
from bson import ObjectId
from datetime import datetime
from app.services import job_service

job_applications = database.get_collection("job_applications")
favorites_collection = database.get_collection("favorites")
reports_collection = database.get_collection("job_reports")

def get_user_id(request: Request) -> str:
    return str(request.state.user["_id"])

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    doc = doc.copy()
    doc["id"] = str(doc.pop("_id", doc.get("id", "")))
    if isinstance(doc.get("created_by"), ObjectId):
        doc["created_by"] = str(doc["created_by"])
    return doc

async def apply_for_job(job_id: str, user_id: str, data: dict):
    application = {
        "job_id": job_id,
        "user_id": user_id,
        "cover_letter": data["cover_letter"],
        "proposed_amount": data.get("proposed_amount"),
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    res = await job_applications.insert_one(application)
    application["_id"] = res.inserted_id
    return application

async def get_applications_for_job(job_id: str):
    applications = await job_applications.find({"job_id": job_id}).to_list(None)
    return [serialize_doc(app) for app in applications]

async def get_user_applications(user_id: str):
    apps = await job_applications.find({"user_id": user_id}).to_list(None)
    return [serialize_doc(app) for app in apps]

async def get_application_by_id(application_id: str):
    doc = await job_applications.find_one({"_id": ObjectId(application_id)})
    return serialize_doc(doc) if doc else None

async def update_proposal(application_id: str, data: dict):
    await job_applications.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {
            "cover_letter": data.get("cover_letter"),
            "proposed_amount": data.get("proposed_amount"),
            "updated_at": datetime.utcnow()
        }}
    )
    return await get_application_by_id(application_id)

async def delete_proposal(application_id: str):
    await job_applications.delete_one({"_id": ObjectId(application_id)})

async def get_application_count(job_id: str):
    return await job_applications.count_documents({"job_id": job_id})

async def add_job_to_favorites(job_id: str, user_id: str):
    favorite = {
        "job_id": job_id,
        "user_id": user_id,
        "created_at": datetime.utcnow()
    }
    res = await favorites_collection.insert_one(favorite)
    favorite["_id"] = res.inserted_id
    return serialize_doc(favorite)

async def remove_job_from_favorites(job_id: str, user_id: str):
    await favorites_collection.delete_one({"job_id": job_id, "user_id": user_id})

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

async def is_job_favorited(job_id: str, user_id: str):
    return await favorites_collection.count_documents({"job_id": job_id, "user_id": user_id}) > 0

async def get_favorite_by_job_and_user(job_id: str, user_id: str):
    return await favorites_collection.find_one({"job_id": job_id, "user_id": user_id})


async def create_job_report(job_id: str, reporter_id: str, reason: str):
    report = {
        "job_id": job_id,
        "reporter_id": reporter_id,
        "reason": reason,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    result = await reports_collection.insert_one(report)
    report["_id"] = result.inserted_id
    return serialize_doc(report)

async def get_reports_for_job(job_id: str):
    reports = await reports_collection.find({"job_id": job_id}).to_list(None)
    return [serialize_doc(report) for report in reports]

async def get_user_reports(user_id: str):
    reports = await reports_collection.find({"reporter_id": user_id}).to_list(None)
    return [serialize_doc(report) for report in reports]

async def resolve_report(report_id: str, notes: str):
    await reports_collection.update_one(
        {"_id": ObjectId(report_id)},
        {"$set": {
            "status": "resolved",
            "admin_notes": notes,
            "resolved_at": datetime.utcnow()
        }}
    )
    return await reports_collection.find_one({"_id": ObjectId(report_id)})

async def get_pending_reports():
    reports = await reports_collection.find({"status": "pending"}).to_list(None)
    return [serialize_doc(report) for report in reports]
