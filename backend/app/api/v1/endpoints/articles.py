"""Article endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import Optional
from app.db.session import get_db
from app.models import Article, Claim, NewsSource, Investigation
from app.schemas.article import ArticleResponse, ArticleDetailResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def list_articles(
    source_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List articles with pagination."""
    # Subquery to count completed investigations per article
    investigation_count = (
        db.query(
            Article.id.label("article_id"),
            func.count(Investigation.id).label("investigation_count")
        )
        .outerjoin(Claim, Claim.article_id == Article.id)
        .outerjoin(Investigation, Investigation.claim_id == Claim.id)
        .filter(Investigation.status == "completed")
        .group_by(Article.id)
        .subquery()
    )

    query = db.query(
        Article,
        NewsSource.name.label("source_name"),
        func.count(Claim.id).label("claim_count"),
        func.coalesce(investigation_count.c.investigation_count, 0).label("investigation_count")
    ).outerjoin(NewsSource).outerjoin(Claim).outerjoin(
        investigation_count, investigation_count.c.article_id == Article.id
    ).group_by(Article.id, NewsSource.name, investigation_count.c.investigation_count)

    if source_id:
        query = query.filter(Article.source_id == source_id)
    if status:
        query = query.filter(Article.status == status)

    total = query.count()
    # Sort by investigation count (DESC) first, then by created_at (DESC)
    results = query.order_by(
        func.coalesce(investigation_count.c.investigation_count, 0).desc(),
        Article.created_at.desc()
    ).offset(offset).limit(limit).all()

    items = []
    for article, source_name, claim_count, investigation_count in results:
        article_dict = ArticleResponse.model_validate(article).model_dump()
        article_dict["source_name"] = source_name
        article_dict["claim_count"] = claim_count
        article_dict["investigation_count"] = investigation_count
        items.append(article_dict)

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/{article_id}", response_model=ArticleDetailResponse)
async def get_article(article_id: str, db: Session = Depends(get_db)):
    """Get article details."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Get source name
    source = db.query(NewsSource).filter(NewsSource.id == article.source_id).first()

    # Get claims
    claims = db.query(Claim).filter(Claim.article_id == article_id).all()

    article_dict = ArticleDetailResponse.model_validate(article).model_dump()
    article_dict["source_name"] = source.name if source else None
    article_dict["claims"] = [{"id": str(c.id), "claim_text": c.claim_text, "status": c.status} for c in claims]

    return article_dict
