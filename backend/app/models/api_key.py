"""API Key database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base


class APIKey(Base):
    """API Key model for programmatic access."""

    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key_hash = Column(String(255), nullable=False, unique=True)
    key_prefix = Column(String(10), nullable=False)  # First 8 chars for display
    tier = Column(String(50), default="free")  # 'free', 'pro', 'enterprise'
    rate_limit_per_hour = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime)
    expires_at = Column(DateTime)
    extra_metadata = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<APIKey(prefix='{self.key_prefix}', tier='{self.tier}')>"
