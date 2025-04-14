from bson import ObjectId
from fastapi import HTTPException, status

def validate_object_id(id_str: str) -> bool:
    return ObjectId.is_valid(id_str)

def validate_job_ownership(job: dict, user_id: str) -> None:
    if job["created_by"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this job"
        )

required_fields = {
    'title': {'min': 3, 'max': 100},
    'description': {'min': 10, 'max': 1000},
    'amount': {'min': 0, 'max': 1000000},
    'workplace_type': {'options': ['remote', 'onsite', 'hybrid']},
    'job_type': {'options': ['full-time', 'part-time', 'contract', 'freelance']},
    'experience_level': {'options': ['entry level', 'intermediate', 'expert']},
    'rate_type': {'options': ['hourly', 'daily', 'weekly', 'monthly']}
}

def validate_job_data(job_data: dict) -> None:
    if 'location' in job_data:
        loc = job_data['location']
        if not isinstance(loc, dict) or \
           not all(k in loc for k in ['lat', 'lng']) or \
           not all(isinstance(v, (int, float)) for v in loc.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location must be {'lat': number, 'lng': number}"
            )
            
    for field, rules in required_fields.items():
        if field not in job_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: {field}"
            )
        
        value = job_data[field]
        
        if 'min' in rules and isinstance(value, (str, list)):
            if len(value) < rules['min']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field} must be at least {rules['min']} characters/items"
                )
                
        if 'max' in rules and isinstance(value, (str, list)):
            if len(value) > rules['max']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field} must be at most {rules['max']} characters/items"
                )
                
        if 'options' in rules and value not in rules['options']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid {field}. Must be one of: {', '.join(rules['options'])}"
            )
        if 'min_amount' in job_data and 'max_amount' in job_data:
            if job_data['min_amount'] > job_data['max_amount']:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum amount cannot be greater than maximum amount"
            )