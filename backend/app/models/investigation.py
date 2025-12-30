"""Investigation database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Float, Integer, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base


class Investigation(Base):
    """Investigation model for fact-check investigations."""

    __tablename__ = "investigations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"))
    verdict = Column(String(50))  # 'true', 'mostly_true', 'mixed', 'mostly_false', 'false', 'unverifiable'
    confidence_score = Column(Float)  # 0.0 to 1.0
    summary = Column(Text)  # Human-readable summary of findings
    reasoning = Column(Text)  # LLM reasoning process
    propaganda_signals = Column(JSONB, default=dict)  # Detected propaganda techniques
    source_reliability_avg = Column(Float)  # Average reliability of evidence sources
    evidence_count = Column(Integer, default=0)
    supporting_evidence_count = Column(Integer, default=0)
    refuting_evidence_count = Column(Integer, default=0)
    status = Column(String(50), default="in_progress")  # 'in_progress', 'completed', 'error'
    metadata = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    claim = relationship("Claim", back_populates="investigations")
    evidence = relationship("Evidence", back_populates="investigation", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("ix_investigations_claim", "claim_id"),
        Index("ix_investigations_verdict", "verdict"),
        Index("ix_investigations_confidence", "confidence_score"),
        Index("ix_investigations_status", "status"),
    )

    def __repr__(self):
        return f"<Investigation(verdict='{self.verdict}', confidence={self.confidence_score})>"
