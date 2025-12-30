"""Claim database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Boolean, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base


class Claim(Base):
    """Claim model for extracted factual claims."""

    __tablename__ = "claims"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"))
    claim_text = Column(Text, nullable=False)
    claim_type = Column(String(50))  # 'factual', 'opinion', 'prediction', 'statistic'
    context = Column(Text)  # Surrounding context from article
    is_checkable = Column(Boolean, default=True)
    extraction_confidence = Column(Float)  # 0.0 to 1.0
    status = Column(String(50), default="pending")  # 'pending', 'checking', 'verified', 'error'
    metadata = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    article = relationship("Article", back_populates="claims")
    investigations = relationship("Investigation", back_populates="claim", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("ix_claims_article", "article_id"),
        Index("ix_claims_status", "status"),
        Index("ix_claims_checkable", "is_checkable"),
        Index("ix_claims_type", "claim_type"),
    )

    def __repr__(self):
        return f"<Claim(text='{self.claim_text[:50]}...', type='{self.claim_type}')>"
