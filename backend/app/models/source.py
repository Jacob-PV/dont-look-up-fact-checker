"""News source database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base


class NewsSource(Base):
    """News source model for RSS feeds and news APIs."""

    __tablename__ = "news_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    source_type = Column(String(50), nullable=False)  # 'rss', 'api'
    url = Column(Text, nullable=False)
    reliability_score = Column(Float, default=0.5)  # 0.0 to 1.0
    political_bias = Column(String(50))  # 'left', 'center', 'right', 'unknown'
    is_active = Column(Boolean, default=True)
    fetch_frequency_minutes = Column(Integer, default=60)
    last_fetched_at = Column(DateTime, nullable=True)
    source_metadata = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    articles = relationship("Article", back_populates="source", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<NewsSource(name='{self.name}', type='{self.source_type}')>"
