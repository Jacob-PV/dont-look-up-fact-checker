"""Evidence Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class EvidenceBase(BaseModel):
    """Base evidence schema."""
    source_url: str
    source_name: Optional[str]
    snippet: str
    stance: str  # 'supporting', 'refuting', 'neutral'


class EvidenceCreate(EvidenceBase):
    """Schema for creating evidence."""
    investigation_id: UUID
    source_reliability: Optional[float] = None
    relevance_score: Optional[float] = None


class EvidenceResponse(EvidenceBase):
    """Schema for evidence response."""
    id: UUID
    source_reliability: Optional[float]
    relevance_score: Optional[float]
    published_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
