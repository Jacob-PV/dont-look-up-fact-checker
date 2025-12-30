"""API v1 router."""
from fastapi import APIRouter
from app.api.v1.endpoints import articles, claims, investigations, sources, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(claims.router, prefix="/claims", tags=["claims"])
api_router.include_router(investigations.router, prefix="/investigations", tags=["investigations"])
