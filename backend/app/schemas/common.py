"""Common Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    items: list
    total: int
    limit: int
    offset: int


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
    detail: Optional[str] = None
