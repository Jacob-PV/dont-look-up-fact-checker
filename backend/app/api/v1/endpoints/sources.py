"""News source endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models import NewsSource
from app.schemas.source import NewsSourceResponse, NewsSourceCreate, NewsSourceUpdate
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def list_sources(
    is_active: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all news sources."""
    query = db.query(NewsSource)

    if is_active is not None:
        query = query.filter(NewsSource.is_active == is_active)

    total = query.count()
    sources = query.offset(offset).limit(limit).all()

    return {
        "items": [NewsSourceResponse.model_validate(s) for s in sources],
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.post("", response_model=NewsSourceResponse, status_code=201)
async def create_source(
    source: NewsSourceCreate,
    db: Session = Depends(get_db)
):
    """Create a new news source."""
    db_source = NewsSource(**source.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return NewsSourceResponse.model_validate(db_source)


@router.get("/{source_id}", response_model=NewsSourceResponse)
async def get_source(source_id: str, db: Session = Depends(get_db)):
    """Get a specific news source."""
    source = db.query(NewsSource).filter(NewsSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return NewsSourceResponse.model_validate(source)
