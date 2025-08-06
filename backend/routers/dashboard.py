from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
import models, schemas

router = APIRouter()

@router.post("/log-access", response_model=schemas.UserAccess)
def log_user_access(
    access_data: schemas.UserAccessCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Log user access to the system"""
    # Extract additional information from request if not provided
    if not access_data.ip_address:
        access_data.ip_address = request.client.host
    
    if not access_data.user_agent:
        access_data.user_agent = request.headers.get("user-agent", "")
    
    db_access = models.UserAccess(**access_data.model_dump())
    db.add(db_access)
    db.commit()
    db.refresh(db_access)
    return db_access

@router.get("/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get comprehensive dashboard statistics"""
    
    # User statistics
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(models.User.is_active == True).count()
    
    # Contact statistics
    total_contacts = db.query(models.Contact).count()
    unresolved_contacts = db.query(models.Contact).filter(models.Contact.is_resolved == False).count()
    
    # Item statistics
    total_items = db.query(models.Item).count()
    
    # Recent access (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_access_count = db.query(models.UserAccess).filter(
        models.UserAccess.access_time >= seven_days_ago
    ).count()
    
    # Access by endpoint
    access_by_endpoint = db.query(
        models.UserAccess.endpoint,
        func.count(models.UserAccess.id).label('count')
    ).filter(
        models.UserAccess.endpoint.isnot(None)
    ).group_by(models.UserAccess.endpoint).all()
    
    endpoint_stats = {item.endpoint: item.count for item in access_by_endpoint}
    
    # Access by method
    access_by_method = db.query(
        models.UserAccess.method,
        func.count(models.UserAccess.id).label('count')
    ).filter(
        models.UserAccess.method.isnot(None)
    ).group_by(models.UserAccess.method).all()
    
    method_stats = {item.method: item.count for item in access_by_method}
    
    # Access by status code
    access_by_status = db.query(
        models.UserAccess.status_code,
        func.count(models.UserAccess.id).label('count')
    ).filter(
        models.UserAccess.status_code.isnot(None)
    ).group_by(models.UserAccess.status_code).all()
    
    status_stats = {str(item.status_code): item.count for item in access_by_status}
    
    return schemas.DashboardStats(
        total_users=total_users,
        active_users=active_users,
        total_contacts=total_contacts,
        unresolved_contacts=unresolved_contacts,
        total_items=total_items,
        recent_access_count=recent_access_count,
        access_by_endpoint=endpoint_stats,
        access_by_method=method_stats,
        access_by_status=status_stats
    )

@router.get("/recent-access", response_model=List[schemas.UserAccess])
def get_recent_access(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get recent user access logs"""
    access_logs = db.query(
        models.UserAccess,
        models.User.username,
        models.User.email
    ).join(
        models.User,
        models.UserAccess.user_id == models.User.id,
        isouter=True
    ).order_by(
        desc(models.UserAccess.access_time)
    ).offset(skip).limit(limit).all()
    
    result = []
    for access, username, email in access_logs:
        access_dict = {
            "id": access.id,
            "user_id": access.user_id,
            "access_time": access.access_time,
            "ip_address": access.ip_address,
            "user_agent": access.user_agent,
            "endpoint": access.endpoint,
            "method": access.method,
            "status_code": access.status_code,
            "username": username,
            "email": email
        }
        result.append(schemas.UserAccess(**access_dict))
    
    return result

@router.get("/user-access/{user_id}", response_model=List[schemas.UserAccess])
def get_user_access_history(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get access history for a specific user"""
    access_logs = db.query(models.UserAccess).filter(
        models.UserAccess.user_id == user_id
    ).order_by(
        desc(models.UserAccess.access_time)
    ).offset(skip).limit(limit).all()
    
    return access_logs

@router.delete("/access/{access_id}")
def delete_access_log(access_id: int, db: Session = Depends(get_db)):
    """Delete a specific access log"""
    db_access = db.query(models.UserAccess).filter(models.UserAccess.id == access_id).first()
    if db_access is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access log not found"
        )
    
    db.delete(db_access)
    db.commit()
    return {"message": "Access log deleted successfully"}