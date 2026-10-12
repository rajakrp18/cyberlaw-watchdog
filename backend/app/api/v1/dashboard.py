import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from app.database import get_db
from app.models import Document, DocumentStatus, LawyerReview
from app.schemas import DashboardStats

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)) -> Any:
    """Get high-level statistics for the MVP dashboard."""
    
    # Simple count queries
    new_devs = await db.scalar(select(func.count(Document.id)).where(Document.status == DocumentStatus.DISCOVERED))
    pending = await db.scalar(select(func.count(Document.id)).where(Document.status == DocumentStatus.PENDING_REVIEW))
    
    # In a full app, these would join with Classification to count P0/P1s
    # For MVP scaffold, returning placeholder zero for complex joins
    return DashboardStats(
        new_developments=new_devs or 0,
        ai_filtered=0,  # Would join classifications
        pending_review=pending or 0,
        action_required=0,
        p0_count=0,
        p1_count=0,
        approved_to_kb=0
    )
