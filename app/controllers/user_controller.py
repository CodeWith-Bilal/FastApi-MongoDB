from fastapi import APIRouter, Depends, HTTPException, status
from app.services import user_service
from app.models.user_model import UserCreate, UserUpdate, UserResponse
from typing import List

async def create_user(user: UserCreate):
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    return await user_service.create_user(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
        skills=user.skills,
        description=user.description,
        address=user.address,
        phone_number=user.phone_number,
        gender=user.gender,
        date_of_birth=user.date_of_birth,
        title=user.title,
        company=user.company,
        employment_history=user.employment_history,
        education_info=user.education_info,
        portfolio=user.portfolio,
        certificates_and_licenses=user.certificates_and_licenses,
        languages=user.languages,
        job_preferences=user.job_preferences
    )

async def get_all_users():
    return await user_service.get_all_users()

async def update_user(user_id: str, user_update: UserUpdate, current_user_email: str):
    update_data = user_update.dict(exclude_unset=True)
    
    return await user_service.update_user(
        user_id=user_id,
        update_data=update_data,
        current_user_email=current_user_email
    )

async def delete_user(user_id: str, current_user_email: str):
    return await user_service.delete_user(
        user_id=user_id,
        current_user_email=current_user_email
    )

async def get_user_by_email(email: str):
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user