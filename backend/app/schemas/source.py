"""News source Pydantic schemas."""
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from uuid import UUID


class NewsSourceBase(BaseModel):
    """Base news source schema."""
    name: str
    source_type: str  # 'rss', 'api'
    url: str
    reliability_score: float = 0.5
    political_bias: Optional[str] = None
    fetch_frequency_minutes: int = 60


class NewsSourceCreate(NewsSourceBase):
    """Schema for creating a news source."""
    pass


class NewsSourceUpdate(BaseModel):
    """Schema for updating a news source."""
    name: Optional[str] = None
    is_active: Optional[bool] = None
    reliability_score: Optional[float] = None
    fetch_frequency_minutes: Optional[int] = None


class NewsSourceResponse(NewsSourceBase):
    """Schema for news source response."""
    id: UUID
    is_active: bool
    last_fetched_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
