"""Claim endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.models import Claim, Article, Investigation
from app.schemas.claim import ClaimResponse, ClaimDetailResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def list_claims(
    article_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List claims with pagination."""
    query = db.query(Claim)

    if article_id:
        query = query.filter(Claim.article_id == article_id)
    if status:
        query = query.filter(Claim.status == status)

    total = query.count()
    claims = query.offset(offset).limit(limit).all()

    return {
        "items": [ClaimResponse.model_validate(c) for c in claims],
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/{claim_id}", response_model=ClaimDetailResponse)
async def get_claim(claim_id: str, db: Session = Depends(get_db)):
    """Get claim details with investigation."""
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    # Get article title
    article = db.query(Article).filter(Article.id == claim.article_id).first()

    # Get investigation
    investigation = db.query(Investigation).filter(Investigation.claim_id == claim_id).first()

    claim_dict = ClaimDetailResponse.model_validate(claim).model_dump()
    claim_dict["article_title"] = article.title if article else None
    if investigation:
        claim_dict["investigation"] = {
            "id": str(investigation.id),
            "verdict": investigation.verdict,
            "confidence_score": investigation.confidence_score,
            "summary": investigation.summary,
            "evidence_count": investigation.evidence_count
        }

    return claim_dict
