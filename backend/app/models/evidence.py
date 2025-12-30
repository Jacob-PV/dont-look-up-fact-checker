"""Evidence database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base


class Evidence(Base):
    """Evidence model for evidence found for/against claims."""

    __tablename__ = "evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"))
    source_url = Column(Text, nullable=False)
    source_name = Column(String(255))
    source_reliability = Column(Float)  # 0.0 to 1.0
    snippet = Column(Text)  # Relevant excerpt
    context = Column(Text)  # Additional context
    stance = Column(String(50))  # 'supporting', 'refuting', 'neutral'
    relevance_score = Column(Float)  # 0.0 to 1.0
    published_at = Column(DateTime)
    embedding_id = Column(String(255))  # Reference to FAISS index
    metadata = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    investigation = relationship("Investigation", back_populates="evidence")

    # Indexes
    __table_args__ = (
        Index("ix_evidence_investigation", "investigation_id"),
        Index("ix_evidence_stance", "stance"),
        Index("ix_evidence_relevance", "relevance_score"),
        Index("ix_evidence_reliability", "source_reliability"),
    )

    def __repr__(self):
        return f"<Evidence(source='{self.source_name}', stance='{self.stance}')>"
