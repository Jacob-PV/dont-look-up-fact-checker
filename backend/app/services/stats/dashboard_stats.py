"""Dashboard statistics service."""
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.article import Article
from app.models.claim import Claim
from app.models.investigation import Investigation


def parse_time_range(time_range: str) -> int:
    """Parse time range string to hours.

    Args:
        time_range: Time range string ('24h', '7d', '30d')

    Returns:
        Number of hours
    """
    if time_range == "24h":
        return 24
    elif time_range == "7d":
        return 168  # 7 * 24
    elif time_range == "30d":
        return 720  # 30 * 24
    return 24  # default


def get_dashboard_overview(db: Session, time_range: str = "24h") -> Dict:
    """Get complete dashboard statistics.

    Args:
        db: Database session
        time_range: Time range for recent activity ('24h', '7d', '30d')

    Returns:
        Dictionary with all dashboard statistics
    """
    hours = parse_time_range(time_range)

    # Get overview stats
    total_articles = db.query(Article).count()
    total_claims = db.query(Claim).count()
    total_investigations = db.query(Investigation).count()

    # Get last ingestion time
    last_article = db.query(Article).order_by(Article.created_at.desc()).first()
    last_ingestion = last_article.created_at.isoformat() if last_article else None

    # Build complete response
    return {
        "overview": {
            "total_articles": total_articles,
            "total_claims": total_claims,
            "total_investigations": total_investigations,
            "last_ingestion": last_ingestion
        },
        "verdict_distribution": calculate_verdict_distribution(db),
        "recent_activity": get_recent_activity(db, hours),
        "quality_metrics": calculate_quality_metrics(db),
        "processing_queue": get_processing_queue_status(db),
        "trending_claims": get_trending_claims(db, limit=5),
        "propaganda_analysis": analyze_propaganda_patterns(db)
    }


def calculate_verdict_distribution(db: Session) -> Dict:
    """Count investigations by verdict type.

    Args:
        db: Database session

    Returns:
        Dictionary with verdict counts
    """
    verdicts = db.query(
        Investigation.verdict,
        func.count(Investigation.id)
    ).group_by(Investigation.verdict).all()

    verdict_map = {v: count for v, count in verdicts if v}

    return {
        "true": verdict_map.get("true", 0),
        "mostly_true": verdict_map.get("mostly_true", 0),
        "mixed": verdict_map.get("mixed", 0),
        "mostly_false": verdict_map.get("mostly_false", 0),
        "false": verdict_map.get("false", 0),
        "unverifiable": verdict_map.get("unverifiable", 0)
    }


def get_recent_activity(db: Session, hours: int) -> Dict:
    """Count items created in the last N hours.

    Args:
        db: Database session
        hours: Number of hours to look back

    Returns:
        Dictionary with recent activity counts
    """
    cutoff = datetime.utcnow() - timedelta(hours=hours)

    new_articles = db.query(Article).filter(Article.created_at >= cutoff).count()
    new_claims = db.query(Claim).filter(Claim.created_at >= cutoff).count()
    new_investigations = db.query(Investigation).filter(Investigation.created_at >= cutoff).count()

    # Format time range label
    if hours < 48:
        time_range_label = f"{hours}h"
    else:
        time_range_label = f"{hours // 24}d"

    return {
        "time_range": time_range_label,
        "new_articles": new_articles,
        "new_claims": new_claims,
        "new_investigations": new_investigations
    }


def calculate_quality_metrics(db: Session) -> Dict:
    """Calculate average quality scores.

    Args:
        db: Database session

    Returns:
        Dictionary with quality metrics
    """
    # Average confidence from investigations
    avg_confidence = db.query(func.avg(Investigation.confidence_score)).scalar() or 0.0

    # Average source reliability
    avg_reliability = db.query(func.avg(Investigation.source_reliability_avg)).scalar() or 0.0

    # Calculate avg propaganda score from propaganda_signals JSONB
    investigations = db.query(Investigation).all()
    total_propaganda = 0
    count = 0

    for inv in investigations:
        if inv.propaganda_signals and isinstance(inv.propaganda_signals, dict):
            techniques = inv.propaganda_signals.get('techniques', [])
            if techniques:
                total_propaganda += len(techniques)
                count += 1

    # Normalize to 0-1 scale (assuming max 10 techniques per investigation)
    avg_propaganda_score = (total_propaganda / count / 10) if count > 0 else 0.0
    avg_propaganda_score = min(avg_propaganda_score, 1.0)  # Cap at 1.0

    return {
        "avg_confidence": round(avg_confidence, 2),
        "avg_propaganda_score": round(avg_propaganda_score, 2),
        "avg_source_reliability": round(avg_reliability, 2)
    }


def get_processing_queue_status(db: Session) -> Dict:
    """Get current processing queue status.

    Args:
        db: Database session

    Returns:
        Dictionary with queue status
    """
    return {
        "pending_articles": db.query(Article).filter(Article.status == "pending").count(),
        "processing_articles": db.query(Article).filter(Article.status == "processing").count(),
        "pending_claims": db.query(Claim).filter(Claim.status == "pending").count(),
        "checking_claims": db.query(Claim).filter(Claim.status == "checking").count()
    }


def get_trending_claims(db: Session, limit: int = 5) -> List[Dict]:
    """Get most frequently verified claims.

    Args:
        db: Database session
        limit: Maximum number of claims to return

    Returns:
        List of trending claim dictionaries
    """
    # Get high-confidence investigations
    investigations = db.query(Investigation).join(Claim).filter(
        Investigation.confidence_score >= 0.7
    ).order_by(Investigation.confidence_score.desc()).limit(limit * 2).all()  # Get extra to filter

    trending = []
    seen_texts = set()

    for inv in investigations:
        if len(trending) >= limit:
            break

        claim = db.query(Claim).filter(Claim.id == inv.claim_id).first()
        if not claim or claim.claim_text in seen_texts:
            continue

        seen_texts.add(claim.claim_text)

        # Count articles from same source (simplified trending metric)
        article_count = 1
        if claim.article and claim.article.source:
            article_count = db.query(Article).filter(
                Article.source_id == claim.article.source_id
            ).count()
            article_count = min(article_count, 10)  # Cap for display

        trending.append({
            "claim_text": claim.claim_text,
            "verdict": inv.verdict or "unknown",
            "confidence": float(inv.confidence_score) if inv.confidence_score else 0.0,
            "article_count": article_count
        })

    return trending


def analyze_propaganda_patterns(db: Session) -> Dict:
    """Analyze propaganda techniques and problematic sources.

    Args:
        db: Database session

    Returns:
        Dictionary with propaganda analysis
    """
    investigations = db.query(Investigation).all()

    # Count techniques
    technique_counts = {}
    source_data = {}

    for inv in investigations:
        # Extract techniques
        if inv.propaganda_signals and isinstance(inv.propaganda_signals, dict):
            techniques = inv.propaganda_signals.get('techniques', [])
            for tech in techniques:
                if isinstance(tech, str):
                    technique_counts[tech] = technique_counts.get(tech, 0) + 1

        # Aggregate source data
        claim = db.query(Claim).filter(Claim.id == inv.claim_id).first()
        if claim and claim.article and claim.article.source:
            source_name = claim.article.source.name

            if source_name not in source_data:
                source_data[source_name] = {
                    "total_techniques": 0,
                    "count": 0,
                    "articles": set()
                }

            # Count techniques for this source
            if inv.propaganda_signals and isinstance(inv.propaganda_signals, dict):
                tech_count = len(inv.propaganda_signals.get('techniques', []))
                source_data[source_name]["total_techniques"] += tech_count

            source_data[source_name]["count"] += 1
            source_data[source_name]["articles"].add(str(claim.article_id))

    # Build top techniques list
    top_techniques = [
        {"technique": k, "count": v}
        for k, v in sorted(technique_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    # Build problematic sources list
    problematic_sources = []
    for name, data in source_data.items():
        if data["count"] > 0:
            # Calculate propaganda score (normalized to 0-1)
            avg_techniques = data["total_techniques"] / data["count"]
            propaganda_score = min(avg_techniques / 10, 1.0)  # Normalize, cap at 1.0

            problematic_sources.append({
                "source_name": name,
                "propaganda_score": round(propaganda_score, 2),
                "article_count": len(data["articles"])
            })

    # Sort by score and take top 5
    problematic_sources.sort(key=lambda x: x["propaganda_score"], reverse=True)
    problematic_sources = problematic_sources[:5]

    return {
        "top_techniques": top_techniques,
        "problematic_sources": problematic_sources
    }
