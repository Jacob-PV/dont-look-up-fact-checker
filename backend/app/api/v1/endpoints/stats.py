"""Stats API endpoints."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.stats.dashboard_stats import get_dashboard_overview
from app.schemas.stats import DashboardStatsResponse
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_redis():
    """Get Redis connection.

    Returns:
        Redis connection or None if unavailable
    """
    try:
        import redis
        from app.core.config import settings

        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        return r
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")
        return None


@router.get("/overview", response_model=DashboardStatsResponse)
def get_stats_overview(
    time_range: str = Query(default="24h", regex="^(24h|7d|30d)$"),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard statistics.

    Args:
        time_range: Time range for recent activity ('24h', '7d', '30d')
        db: Database session

    Returns:
        Complete dashboard statistics

    Raises:
        HTTPException: If stats calculation fails
    """
    try:
        # Try cache first
        redis_client = get_redis()
        cache_key = f"dashboard:stats:{time_range}"

        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    logger.info(f"Returning cached stats for {time_range}")
                    return json.loads(cached)
            except Exception as e:
                logger.warning(f"Redis get failed: {e}")

        # Calculate stats
        logger.info(f"Calculating dashboard stats for {time_range}")
        stats = get_dashboard_overview(db, time_range)

        # Cache for 5 minutes
        if redis_client:
            try:
                redis_client.setex(cache_key, 300, json.dumps(stats))
                logger.info(f"Cached stats for {time_range}")
            except Exception as e:
                logger.warning(f"Redis setex failed: {e}")

        return stats

    except Exception as e:
        logger.error(f"Error calculating dashboard stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error calculating dashboard statistics"
        )
