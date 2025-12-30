"""Article database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base


class Article(Base):
    """Article model for ingested news articles."""

    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("news_sources.id", ondelete="CASCADE"))
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False, unique=True)
    author = Column(String(255))
    published_at = Column(DateTime)
    content = Column(Text)  # Full article text (PII redacted)
    content_hash = Column(String(64))  # SHA-256 hash for deduplication
    status = Column(String(50), default="pending")  # 'pending', 'processing', 'analyzed', 'error'
    metadata = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source = relationship("NewsSource", back_populates="articles")
    claims = relationship("Claim", back_populates="article", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("ix_articles_source", "source_id"),
        Index("ix_articles_published", "published_at"),
        Index("ix_articles_status", "status"),
        Index("ix_articles_hash", "content_hash"),
        Index("ix_articles_url", "url"),
    )

    def __repr__(self):
        return f"<Article(title='{self.title[:50]}...', status='{self.status}')>"
