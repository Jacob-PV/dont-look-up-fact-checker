"""Investigation endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.models import Investigation, Claim, Evidence, Article
from app.schemas.investigation import InvestigationResponse, InvestigationDetailResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def list_investigations(
    verdict: Optional[str] = None,
    min_confidence: Optional[float] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List investigations with pagination."""
    query = db.query(Investigation)

    if verdict:
        query = query.filter(Investigation.verdict == verdict)
    if min_confidence:
        query = query.filter(Investigation.confidence_score >= min_confidence)

    total = query.count()
    investigations = query.offset(offset).limit(limit).all()

    # Add claim text and article info to each investigation
    items = []
    for inv in investigations:
        claim = db.query(Claim).filter(Claim.id == inv.claim_id).first()
        inv_dict = InvestigationResponse.model_validate(inv).model_dump()
        inv_dict["claim_text"] = claim.claim_text if claim else None

        # Add article information
        if claim and claim.article_id:
            article = db.query(Article).filter(Article.id == claim.article_id).first()
            if article:
                inv_dict["article_id"] = str(article.id)
                inv_dict["article_title"] = article.title
                inv_dict["article_url"] = article.url

        items.append(inv_dict)

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/{investigation_id}", response_model=InvestigationDetailResponse)
async def get_investigation(investigation_id: str, db: Session = Depends(get_db)):
    """Get investigation details with evidence."""
    investigation = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")

    # Get claim
    claim = db.query(Claim).filter(Claim.id == investigation.claim_id).first()

    # Get evidence
    evidence = db.query(Evidence).filter(Evidence.investigation_id == investigation_id).all()

    inv_dict = InvestigationDetailResponse.model_validate(investigation).model_dump()
    inv_dict["claim_text"] = claim.claim_text if claim else None

    # Add article information
    if claim and claim.article_id:
        article = db.query(Article).filter(Article.id == claim.article_id).first()
        if article:
            inv_dict["article_id"] = str(article.id)
            inv_dict["article_title"] = article.title
            inv_dict["article_url"] = article.url

    inv_dict["evidence"] = [
        {
            "id": str(e.id),
            "source_name": e.source_name,
            "source_url": e.source_url,
            "snippet": e.snippet,
            "stance": e.stance,
            "relevance_score": e.relevance_score,
            "source_reliability": e.source_reliability
        }
        for e in evidence
    ]

    return inv_dict
