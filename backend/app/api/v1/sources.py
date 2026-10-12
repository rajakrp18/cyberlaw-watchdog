import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import Source
from app.schemas import SourceResponse, SourceCreate

router = APIRouter()

@router.get("/", response_model=List[SourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)) -> Any:
    """Retrieve all approved sources."""
    result = await db.execute(select(Source).order_by(Source.name))
    return result.scalars().all()

@router.post("/", response_model=SourceResponse)
async def create_source(source_in: SourceCreate, db: AsyncSession = Depends(get_db)) -> Any:
    """Register a new source."""
    source = Source(**source_in.model_dump())
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source
