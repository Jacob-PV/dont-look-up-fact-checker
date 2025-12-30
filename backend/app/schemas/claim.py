"""Claim Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class ClaimBase(BaseModel):
    """Base claim schema."""
    claim_text: str
    claim_type: Optional[str] = None
    context: Optional[str] = None
    is_checkable: bool = True


class ClaimCreate(ClaimBase):
    """Schema for creating a claim."""
    article_id: UUID
    extraction_confidence: Optional[float] = None


class ClaimResponse(ClaimBase):
    """Schema for claim response."""
    id: UUID
    article_id: UUID
    extraction_confidence: Optional[float]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ClaimDetailResponse(ClaimResponse):
    """Schema for detailed claim response."""
    article_title: Optional[str] = None
    investigation: Optional[dict] = None
