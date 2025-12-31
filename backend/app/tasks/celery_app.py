"""Celery application configuration."""
import os
from celery import Celery
from celery.schedules import crontab

# Get environment variables
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

# Create Celery app
celery_app = Celery(
    "factcheck",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks.rss_tasks", "app.tasks.claim_tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max per task
    task_soft_time_limit=240,  # Soft limit at 4 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Periodic task schedule using Celery Beat
celery_app.conf.beat_schedule = {
    "fetch-rss-feeds-every-30-minutes": {
        "task": "app.tasks.rss_tasks.fetch_all_rss_feeds",
        "schedule": crontab(minute="*/30"),  # Every 30 minutes
        "options": {"queue": "rss_ingestion"}
    },
    "extract-claims-every-5-minutes": {
        "task": "app.tasks.claim_tasks.process_pending_articles",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
        "options": {"queue": "claim_extraction"}
    },
    "fact-check-claims-every-10-minutes": {
        "task": "app.tasks.claim_tasks.process_pending_claims",
        "schedule": crontab(minute="*/10"),  # Every 10 minutes
        "options": {"queue": "fact_checking"}
    },
}

# Optional: Set default queue name
celery_app.conf.task_default_queue = "default"
