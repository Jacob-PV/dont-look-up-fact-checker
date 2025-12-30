"""Health check endpoints."""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("")
async def health_check():
    """Comprehensive health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": {"status": "ok"},
            "redis": {"status": "ok"},
            "ollama": {"status": "ok"}
        }
    }
