"""Pydantic schemas for dashboard statistics."""
from typing import List, Optional
from pydantic import BaseModel


class OverviewStats(BaseModel):
    """Overview statistics model."""
    total_articles: int
    total_claims: int
    total_investigations: int
    last_ingestion: Optional[str] = None


class VerdictDistribution(BaseModel):
    """Verdict distribution model."""
    true: int = 0
    mostly_true: int = 0
    mixed: int = 0
    mostly_false: int = 0
    false: int = 0
    unverifiable: int = 0


class RecentActivity(BaseModel):
    """Recent activity model."""
    time_range: str
    new_articles: int
    new_claims: int
    new_investigations: int


class QualityMetrics(BaseModel):
    """Quality metrics model."""
    avg_confidence: float
    avg_propaganda_score: float
    avg_source_reliability: float


class ProcessingQueue(BaseModel):
    """Processing queue status model."""
    pending_articles: int
    processing_articles: int
    pending_claims: int
    checking_claims: int


class TrendingClaim(BaseModel):
    """Trending claim model."""
    claim_text: str
    verdict: str
    confidence: float
    article_count: int


class PropagandaTechnique(BaseModel):
    """Propaganda technique model."""
    technique: str
    count: int


class ProblematicSource(BaseModel):
    """Problematic source model."""
    source_name: str
    propaganda_score: float
    article_count: int


class PropagandaAnalysis(BaseModel):
    """Propaganda analysis model."""
    top_techniques: List[PropagandaTechnique]
    problematic_sources: List[ProblematicSource]


class DashboardStatsResponse(BaseModel):
    """Complete dashboard statistics response model."""
    overview: OverviewStats
    verdict_distribution: VerdictDistribution
    recent_activity: RecentActivity
    quality_metrics: QualityMetrics
    processing_queue: ProcessingQueue
    trending_claims: List[TrendingClaim]
    propaganda_analysis: PropagandaAnalysis
