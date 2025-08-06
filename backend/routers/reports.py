from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
from services.pdf_service import pdf_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/users", response_class=Response)
async def generate_users_report(db: Session = Depends(get_db)):
    """
    Generate PDF report for all users
    """
    try:
        logger.info("Generating users PDF report")
        
        # Get all users from database
        users = db.query(models.User).all()
        
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found in the database"
            )
        
        # Generate PDF
        pdf_content = pdf_service.generate_users_report(users)
        
        logger.info(f"Users PDF report generated successfully for {len(users)} users")
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=users_report.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating users report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )

@router.get("/items", response_class=Response)
async def generate_items_report(db: Session = Depends(get_db)):
    """
    Generate PDF report for all items
    """
    try:
        logger.info("Generating items PDF report")
        
        # Get all items from database
        items = db.query(models.Item).all()
        
        if not items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No items found in the database"
            )
        
        # Generate PDF
        pdf_content = pdf_service.generate_items_report(items)
        
        logger.info(f"Items PDF report generated successfully for {len(items)} items")
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=items_report.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating items report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )

@router.get("/comprehensive", response_class=Response)
async def generate_comprehensive_report(db: Session = Depends(get_db)):
    """
    Generate comprehensive PDF report with both users and items
    """
    try:
        logger.info("Generating comprehensive PDF report")
        
        # Get all users and items from database
        users = db.query(models.User).all()
        items = db.query(models.Item).all()
        
        if not users and not items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No data found in the database"
            )
        
        # Generate PDF
        pdf_content = pdf_service.generate_comprehensive_report(users, items)
        
        logger.info(f"Comprehensive PDF report generated successfully for {len(users)} users and {len(items)} items")
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=comprehensive_report.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating comprehensive report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )

@router.get("/health")
async def reports_health_check():
    """
    Health check endpoint for reports service
    """
    return {
        "status": "healthy",
        "service": "PDF Reports",
        "version": "1.0.0"
    }