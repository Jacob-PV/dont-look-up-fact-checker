"""RSS feed fetching and article ingestion service."""
import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Optional
from time import mktime

import feedparser
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.source import NewsSource
from app.models.article import Article
from app.services.analysis.influence_scorer import InfluenceScorer

# Set up logging
logger = logging.getLogger(__name__)


def calculate_content_hash(content: str) -> str:
    """
    Generate SHA-256 hash of content for deduplication.

    Args:
        content: Article content to hash

    Returns:
        Hexadecimal hash string
    """
    if not content:
        return ""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def redact_article_content(content: str) -> str:
    """
    Redact personally identifiable information from article content.

    Args:
        content: Raw article content

    Returns:
        Content with PII redacted
    """
    try:
        from app.services.privacy.pii_detector import PIIRedactor
        redactor = PIIRedactor()
        redacted_text, count = redactor.redact(content)
        if count > 0:
            logger.info(f"Redacted {count} PII entities from article content")
        return redacted_text
    except ImportError:
        logger.warning("PII redaction service not available, skipping redaction")
        return content
    except Exception as e:
        logger.error(f"Error during PII redaction: {e}")
        return content


def fetch_rss_feed(source_url: str) -> List[Dict]:
    """
    Fetch and parse RSS feed from a URL.

    Args:
        source_url: RSS feed URL

    Returns:
        List of parsed feed entries

    Raises:
        Exception: If feed cannot be fetched or parsed
    """
    try:
        logger.info(f"Fetching RSS feed from: {source_url}")

        # Parse the RSS feed
        feed = feedparser.parse(source_url)

        # Check for errors
        if hasattr(feed, 'bozo') and feed.bozo:
            if hasattr(feed, 'bozo_exception'):
                logger.warning(f"RSS feed has issues: {feed.bozo_exception}")

        # Get entries
        entries = feed.get('entries', [])
        logger.info(f"Found {len(entries)} entries in RSS feed")

        return entries

    except Exception as e:
        logger.error(f"Error fetching RSS feed from {source_url}: {e}")
        raise


def parse_published_date(entry: Dict) -> Optional[datetime]:
    """
    Parse published date from RSS entry.

    Args:
        entry: RSS feed entry dictionary

    Returns:
        Parsed datetime or None if not available
    """
    # Try different date fields
    date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']

    for field in date_fields:
        if field in entry and entry[field]:
            try:
                return datetime.fromtimestamp(mktime(entry[field]))
            except (TypeError, ValueError, OverflowError) as e:
                logger.warning(f"Error parsing date from {field}: {e}")
                continue

    return None


def extract_article_content(entry: Dict) -> str:
    """
    Extract article content from RSS entry.

    Args:
        entry: RSS feed entry dictionary

    Returns:
        Extracted content text
    """
    # Try different content fields in order of preference
    if 'content' in entry and len(entry.content) > 0:
        return entry.content[0].get('value', '')

    if 'summary' in entry:
        return entry.summary

    if 'description' in entry:
        return entry.description

    return ""


def fetch_and_store_articles(source: NewsSource, db: Session) -> int:
    """
    Fetch articles from RSS source and store them in the database.

    Args:
        source: NewsSource model instance
        db: Database session

    Returns:
        Count of new articles added

    Raises:
        Exception: If critical error occurs during fetching
    """
    new_articles_count = 0

    try:
        # Fetch RSS feed entries
        entries = fetch_rss_feed(source.url)

        for entry in entries:
            try:
                # Extract article URL (required)
                article_url = entry.get('link', '').strip()
                if not article_url:
                    logger.warning("Skipping entry without URL")
                    continue

                # Check if article already exists by URL
                existing_article = db.query(Article).filter(
                    Article.url == article_url
                ).first()

                if existing_article:
                    logger.debug(f"Article already exists: {article_url}")
                    continue

                # Extract article data
                title = entry.get('title', 'Untitled').strip()
                author = entry.get('author', '').strip() or None
                published_at = parse_published_date(entry)

                # Extract and process content
                raw_content = extract_article_content(entry)

                # Redact PII from content
                redacted_content = redact_article_content(raw_content)

                # Calculate content hash for deduplication
                content_hash = calculate_content_hash(redacted_content)

                # Create new article
                new_article = Article(
                    source_id=source.id,
                    title=title,
                    url=article_url,
                    author=author,
                    published_at=published_at,
                    content=redacted_content,
                    content_hash=content_hash,
                    status="pending"
                )

                # Calculate and set influence score
                scorer = InfluenceScorer()
                new_article.influence_score = scorer.calculate_influence_score(new_article, source)

                db.add(new_article)
                new_articles_count += 1
                logger.info(f"Added new article: {title[:50]}...")

            except IntegrityError as e:
                # Handle unique constraint violations (duplicate URLs)
                db.rollback()
                logger.warning(f"Duplicate article detected: {e}")
                continue

            except Exception as e:
                # Log error but continue processing other entries
                logger.error(f"Error processing RSS entry: {e}")
                continue

        # Update source's last_fetched_at timestamp
        source.last_fetched_at = datetime.utcnow()

        # Commit all changes
        db.commit()

        logger.info(
            f"Successfully fetched {new_articles_count} new articles from {source.name}"
        )

        return new_articles_count

    except Exception as e:
        db.rollback()
        logger.error(f"Error fetching articles from {source.name}: {e}")
        raise
