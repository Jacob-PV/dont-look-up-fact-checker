"""Article Pydantic schemas."""
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ArticleBase(BaseModel):
    """Base article schema."""
    title: str
    url: str
    author: Optional[str] = None
    published_at: Optional[datetime] = None


class ArticleCreate(ArticleBase):
    """Schema for creating an article."""
    source_id: UUID
    content: Optional[str] = None


class ArticleResponse(ArticleBase):
    """Schema for article response."""
    id: UUID
    source_id: UUID
    source_name: Optional[str] = None
    status: str
    claim_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleDetailResponse(ArticleResponse):
    """Schema for detailed article response."""
    content: Optional[str] = None
    claims: List = []
