"""Investigation Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class InvestigationBase(BaseModel):
    """Base investigation schema."""
    verdict: str
    confidence_score: float
    summary: str


class InvestigationCreate(InvestigationBase):
    """Schema for creating an investigation."""
    claim_id: UUID
    reasoning: Optional[str] = None


class InvestigationResponse(InvestigationBase):
    """Schema for investigation response."""
    id: UUID
    claim_id: UUID
    claim_text: Optional[str] = None
    evidence_count: int = 0
    supporting_evidence_count: int = 0
    refuting_evidence_count: int = 0
    propaganda_signals: dict = {}
    status: str
    created_at: datetime
    updated_at: datetime
    # Article information
    article_id: Optional[str] = None
    article_title: Optional[str] = None
    article_url: Optional[str] = None

    class Config:
        from_attributes = True


class InvestigationDetailResponse(InvestigationResponse):
    """Schema for detailed investigation response."""
    reasoning: Optional[str]
    evidence: List = []
