"""Celery tasks for claim extraction and fact-checking."""
import logging
from uuid import UUID
from typing import Dict, List
from sqlalchemy.exc import SQLAlchemyError

from app.tasks.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.article import Article
from app.models.claim import Claim
from app.models.investigation import Investigation
from app.models.evidence import Evidence
from app.services.analysis.claim_extractor import ClaimExtractor
from app.services.analysis.fact_checker import FactChecker
from app.services.analysis.influence_scorer import InfluenceScorer
from app.services.analysis.evidence_searcher import EvidenceSearcher
from app.services.analysis.propaganda_detector import PropagandaDetector
import asyncio

# Set up logging
logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name="app.tasks.claim_tasks.extract_claims_from_article",
    max_retries=3,
    default_retry_delay=60
)
def extract_claims_from_article(self, article_id: str) -> Dict[str, any]:
    """
    Extract claims from a single article.

    Args:
        article_id: UUID string of the Article

    Returns:
        Dictionary with task results including claims extracted count
    """
    db = SessionLocal()

    try:
        article_uuid = UUID(article_id)
        logger.info(f"Extracting claims from article: {article_id}")

        # Load article
        article = db.query(Article).filter(Article.id == article_uuid).first()

        if not article:
            logger.error(f"Article not found: {article_id}")
            return {
                "success": False,
                "article_id": article_id,
                "error": "Article not found",
                "claims_extracted": 0
            }

        # Update article status
        article.status = "processing"
        db.commit()

        # Extract claims (async operation)
        extractor = ClaimExtractor()
        claims = asyncio.run(extractor.extract_claims(article, db))

        # Save claims to database
        for claim in claims:
            db.add(claim)

        # Update article status
        article.status = "processed" if claims else "error"
        db.commit()

        logger.info(f"Extracted {len(claims)} claims from article {article_id}")

        return {
            "success": True,
            "article_id": article_id,
            "claims_extracted": len(claims)
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error extracting claims: {e}")

        try:
            raise self.retry(exc=e)
        except self.MaxRetriesExceededError:
            # Update article to error status
            article = db.query(Article).filter(Article.id == UUID(article_id)).first()
            if article:
                article.status = "error"
                db.commit()

            return {
                "success": False,
                "article_id": article_id,
                "error": f"Database error: {str(e)}",
                "claims_extracted": 0
            }

    except Exception as e:
        logger.error(f"Error extracting claims: {e}", exc_info=True)

        try:
            raise self.retry(exc=e)
        except self.MaxRetriesExceededError:
            return {
                "success": False,
                "article_id": article_id,
                "error": str(e),
                "claims_extracted": 0
            }

    finally:
        db.close()


@celery_app.task(
    bind=True,
    name="app.tasks.claim_tasks.process_pending_articles"
)
def process_pending_articles(self) -> Dict[str, any]:
    """
    Process all pending articles for claim extraction.

    Prioritizes articles by influence_score (highest first) - priority queue system.

    Returns:
        Dictionary with summary of queued tasks
    """
    db = SessionLocal()

    try:
        logger.info("Processing pending articles for claim extraction")

        # Query pending articles, ordered by influence score (priority queue)
        articles = db.query(Article).filter(
            Article.status == 'pending'
        ).order_by(
            Article.influence_score.desc()
        ).limit(50).all()  # Process max 50 at a time

        if not articles:
            logger.info("No pending articles to process")
            return {
                "success": True,
                "articles_queued": 0,
                "message": "No pending articles"
            }

        # Queue extraction tasks
        task_ids = []
        for article in articles:
            result = extract_claims_from_article.delay(str(article.id))
            task_ids.append(result.id)

        logger.info(f"Queued {len(articles)} articles for claim extraction")

        return {
            "success": True,
            "articles_queued": len(articles),
            "task_ids": task_ids
        }

    except Exception as e:
        logger.error(f"Error processing pending articles: {e}", exc_info=True)
        return {
            "success": False,
            "articles_queued": 0,
            "error": str(e)
        }

    finally:
        db.close()


@celery_app.task(
    bind=True,
    name="app.tasks.claim_tasks.fact_check_claim",
    max_retries=3,
    default_retry_delay=60
)
def fact_check_claim(self, claim_id: str) -> Dict[str, any]:
    """
    Fact-check a single claim.

    Note: This is a placeholder implementation until evidence search is added.
    Currently creates investigations with no evidence.

    Args:
        claim_id: UUID string of the Claim

    Returns:
        Dictionary with task results
    """
    db = SessionLocal()

    try:
        claim_uuid = UUID(claim_id)
        logger.info(f"Fact-checking claim: {claim_id}")

        # Load claim
        claim = db.query(Claim).filter(Claim.id == claim_uuid).first()

        if not claim:
            logger.error(f"Claim not found: {claim_id}")
            return {
                "success": False,
                "claim_id": claim_id,
                "error": "Claim not found"
            }

        # Update claim status
        claim.status = "checking"
        db.commit()

        # 1. Search for evidence
        evidence_searcher = EvidenceSearcher()
        evidence_data = evidence_searcher.search_evidence_for_claim(claim, db, max_results=5)

        # 2. Fact-check claim with evidence (async operation)
        checker = FactChecker()
        investigation = asyncio.run(checker.fact_check_claim(claim, [], db))

        # Save investigation first to get ID
        db.add(investigation)
        db.flush()  # Get investigation.id without committing

        # 3. Create Evidence records linked to investigation
        evidence_list: List[Evidence] = []
        for evidence_item in evidence_data:
            # Determine stance based on verdict (simple heuristic)
            stance = _determine_evidence_stance(
                claim.claim_text,
                evidence_item['snippet'],
                investigation.verdict
            )

            evidence = Evidence(
                investigation_id=investigation.id,
                source_url=evidence_item['source_url'],
                source_name=evidence_item['source_name'],
                source_reliability=0.7,  # Default reliability, can enhance later
                snippet=evidence_item['snippet'],
                context=evidence_item['context'],
                stance=stance,
                relevance_score=evidence_item['relevance_score']
            )
            evidence_list.append(evidence)
            db.add(evidence)

        # 4. Detect propaganda in claim text
        propaganda_detector = PropagandaDetector()
        propaganda_signals = asyncio.run(propaganda_detector.detect_propaganda(
            claim.claim_text
        ))

        # Update investigation with propaganda signals and evidence counts
        investigation.propaganda_signals = propaganda_signals
        investigation.evidence_count = len(evidence_list)
        investigation.supporting_evidence_count = sum(
            1 for e in evidence_list if e.stance == 'supporting'
        )
        investigation.refuting_evidence_count = sum(
            1 for e in evidence_list if e.stance == 'refuting'
        )

        # Update claim status
        claim.status = "verified"

        # Commit all changes
        db.commit()

        logger.info(
            f"Fact-checked claim {claim_id}: "
            f"verdict={investigation.verdict}, "
            f"evidence_count={investigation.evidence_count}, "
            f"propaganda_score={propaganda_signals.get('overall_propaganda_score', 0.0)}"
        )

        return {
            "success": True,
            "claim_id": claim_id,
            "verdict": investigation.verdict,
            "confidence": investigation.confidence_score,
            "evidence_count": investigation.evidence_count,
            "propaganda_score": propaganda_signals.get('overall_propaganda_score', 0.0)
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error fact-checking claim: {e}")

        try:
            raise self.retry(exc=e)
        except self.MaxRetriesExceededError:
            # Update claim to error status
            claim = db.query(Claim).filter(Claim.id == UUID(claim_id)).first()
            if claim:
                claim.status = "error"
                db.commit()

            return {
                "success": False,
                "claim_id": claim_id,
                "error": f"Database error: {str(e)}"
            }

    except Exception as e:
        logger.error(f"Error fact-checking claim: {e}", exc_info=True)

        try:
            raise self.retry(exc=e)
        except self.MaxRetriesExceededError:
            return {
                "success": False,
                "claim_id": claim_id,
                "error": str(e)
            }

    finally:
        db.close()


@celery_app.task(
    bind=True,
    name="app.tasks.claim_tasks.process_pending_claims"
)
def process_pending_claims(self) -> Dict[str, any]:
    """
    Process all pending claims for fact-checking.

    Prioritizes claims from high-influence articles (priority queue system).

    Returns:
        Dictionary with summary of queued tasks
    """
    db = SessionLocal()

    try:
        logger.info("Processing pending claims for fact-checking")

        # Query pending claims, prioritized by article influence score
        claims = db.query(Claim).join(Article).filter(
            Claim.status == 'pending',
            Claim.is_checkable == True
        ).order_by(
            Article.influence_score.desc()
        ).limit(20).all()  # Process max 20 at a time

        if not claims:
            logger.info("No pending claims to process")
            return {
                "success": True,
                "claims_queued": 0,
                "message": "No pending claims"
            }

        # Queue fact-check tasks
        task_ids = []
        for claim in claims:
            result = fact_check_claim.delay(str(claim.id))
            task_ids.append(result.id)

        logger.info(f"Queued {len(claims)} claims for fact-checking")

        return {
            "success": True,
            "claims_queued": len(claims),
            "task_ids": task_ids
        }

    except Exception as e:
        logger.error(f"Error processing pending claims: {e}", exc_info=True)
        return {
            "success": False,
            "claims_queued": 0,
            "error": str(e)
        }

    finally:
        db.close()


@celery_app.task(
    bind=True,
    name="app.tasks.claim_tasks.calculate_article_influence"
)
def calculate_article_influence(self, article_id: str) -> Dict[str, any]:
    """
    Calculate influence score for an article.

    Args:
        article_id: UUID string of the Article

    Returns:
        Dictionary with task results including influence score
    """
    db = SessionLocal()

    try:
        article_uuid = UUID(article_id)

        # Load article with source
        article = db.query(Article).filter(Article.id == article_uuid).first()

        if not article:
            return {
                "success": False,
                "article_id": article_id,
                "error": "Article not found"
            }

        # Calculate influence score
        scorer = InfluenceScorer()
        influence_score = scorer.calculate_influence_score(article, article.source)

        # Update article
        article.influence_score = influence_score
        db.commit()

        logger.info(f"Article {article_id} influence score: {influence_score}")

        return {
            "success": True,
            "article_id": article_id,
            "influence_score": influence_score
        }

    except Exception as e:
        logger.error(f"Error calculating influence: {e}", exc_info=True)
        return {
            "success": False,
            "article_id": article_id,
            "error": str(e)
        }

    finally:
        db.close()


def _determine_evidence_stance(
    claim_text: str,
    evidence_snippet: str,
    verdict: str
) -> str:
    """
    Determine if evidence supports, refutes, or is neutral to claim.

    Simple heuristic based on verdict for MVP.
    Can enhance with LLM analysis later.

    Args:
        claim_text: The claim being fact-checked
        evidence_snippet: Evidence text
        verdict: Investigation verdict

    Returns:
        'supporting', 'refuting', or 'neutral'
    """
    # Simple heuristic: if verdict is positive, evidence is supporting
    # If verdict is negative, evidence is refuting
    # Mixed verdicts have neutral stances
    if verdict in ['true', 'mostly_true']:
        return 'supporting'
    elif verdict in ['false', 'mostly_false']:
        return 'refuting'
    else:
        return 'neutral'
