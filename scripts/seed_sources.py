#!/usr/bin/env python3
"""Seed database with initial news sources."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.db.session import SessionLocal
from app.models import NewsSource

INITIAL_SOURCES = [
    {
        "name": "Reuters",
        "source_type": "rss",
        "url": "https://www.reuters.com/rssFeed/topNews",
        "reliability_score": 0.85,
        "political_bias": "center",
        "fetch_frequency_minutes": 30,
    },
    {
        "name": "Associated Press",
        "source_type": "rss",
        "url": "https://feeds.apnews.com/rss/apf-topnews",
        "reliability_score": 0.88,
        "political_bias": "center",
        "fetch_frequency_minutes": 30,
    },
    {
        "name": "BBC News",
        "source_type": "rss",
        "url": "http://feeds.bbci.co.uk/news/rss.xml",
        "reliability_score": 0.82,
        "political_bias": "center",
        "fetch_frequency_minutes": 30,
    },
    {
        "name": "NPR News",
        "source_type": "rss",
        "url": "https://feeds.npr.org/1001/rss.xml",
        "reliability_score": 0.80,
        "political_bias": "center",
        "fetch_frequency_minutes": 60,
    },
    {
        "name": "The Guardian",
        "source_type": "rss",
        "url": "https://www.theguardian.com/world/rss",
        "reliability_score": 0.78,
        "political_bias": "left",
        "fetch_frequency_minutes": 60,
    },
]


def seed_sources():
    """Seed initial news sources."""
    db = SessionLocal()

    try:
        # Check if sources already exist
        existing = db.query(NewsSource).count()
        if existing > 0:
            print(f"Database already has {existing} sources. Skipping seed.")
            return

        # Add sources
        for source_data in INITIAL_SOURCES:
            source = NewsSource(**source_data)
            db.add(source)
            print(f"Added source: {source_data['name']}")

        db.commit()
        print(f"\nSuccessfully seeded {len(INITIAL_SOURCES)} news sources!")

    except Exception as e:
        print(f"Error seeding sources: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_sources()
