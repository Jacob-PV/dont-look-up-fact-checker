"""Celery tasks for RSS feed ingestion."""
import logging
from uuid import UUID
from typing import Dict

from celery import group
from sqlalchemy.exc import SQLAlchemyError

from app.tasks.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.source import NewsSource
from app.services.ingestion.rss_fetcher import fetch_and_store_articles

# Set up logging
logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name="app.tasks.rss_tasks.fetch_rss_source_articles",
    max_retries=3,
    default_retry_delay=60
)
def fetch_rss_source_articles(self, source_id: str) -> Dict[str, any]:
    """
    Fetch articles from a single RSS source.

    Args:
        source_id: UUID string of the NewsSource

    Returns:
        Dictionary with task results including article count
    """
    db = SessionLocal()

    try:
        # Convert string to UUID
        source_uuid = UUID(source_id)

        logger.info(f"Starting RSS fetch for source: {source_id}")

        # Load NewsSource from database
        source = db.query(NewsSource).filter(NewsSource.id == source_uuid).first()

        if not source:
            logger.error(f"NewsSource not found: {source_id}")
            return {
                "success": False,
                "source_id": source_id,
                "error": "Source not found",
                "articles_added": 0
            }

        if not source.is_active:
            logger.info(f"NewsSource is inactive: {source.name}")
            return {
                "success": False,
                "source_id": source_id,
                "error": "Source is inactive",
                "articles_added": 0
            }

        # Fetch and store articles
        articles_added = fetch_and_store_articles(source, db)

        logger.info(
            f"Successfully fetched {articles_added} articles from {source.name}"
        )

        return {
            "success": True,
            "source_id": source_id,
            "source_name": source.name,
            "articles_added": articles_added
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error fetching RSS source {source_id}: {e}")

        # Retry the task
        try:
            raise self.retry(exc=e)
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for source {source_id}")
            return {
                "success": False,
                "source_id": source_id,
                "error": f"Database error: {str(e)}",
                "articles_added": 0
            }

    except Exception as e:
        logger.error(f"Error fetching RSS source {source_id}: {e}", exc_info=True)

        # Retry the task for transient errors
        try:
            raise self.retry(exc=e)
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for source {source_id}")
            return {
                "success": False,
                "source_id": source_id,
                "error": str(e),
                "articles_added": 0
            }

    finally:
        db.close()


@celery_app.task(
    bind=True,
    name="app.tasks.rss_tasks.fetch_all_rss_feeds"
)
def fetch_all_rss_feeds(self) -> Dict[str, any]:
    """
    Fetch articles from all active RSS sources.

    This is the main periodic task scheduled by Celery Beat.
    It dispatches individual fetch tasks for each active RSS source.

    Returns:
        Dictionary with summary of queued fetch tasks
    """
    db = SessionLocal()

    try:
        logger.info("Starting periodic RSS feed fetch for all active sources")

        # Query all active RSS sources
        sources = db.query(NewsSource).filter(
            NewsSource.is_active == True,
            NewsSource.source_type == 'rss'
        ).all()

        if not sources:
            logger.warning("No active RSS sources found")
            return {
                "success": True,
                "sources_queued": 0,
                "message": "No active RSS sources found"
            }

        # Create a list of task signatures for parallel processing
        task_signatures = []
        for source in sources:
            task_signature = fetch_rss_source_articles.s(str(source.id))
            task_signatures.append(task_signature)

        # Dispatch all tasks as a group for parallel processing
        job = group(task_signatures)
        result = job.apply_async()

        logger.info(
            f"Queued {len(sources)} RSS sources for fetching. Task group ID: {result.id}"
        )

        return {
            "success": True,
            "sources_queued": len(sources),
            "task_group_id": result.id,
            "source_names": [source.name for source in sources]
        }

    except Exception as e:
        logger.error(f"Error queuing RSS feed fetches: {e}", exc_info=True)
        return {
            "success": False,
            "sources_queued": 0,
            "error": str(e)
        }

    finally:
        db.close()
