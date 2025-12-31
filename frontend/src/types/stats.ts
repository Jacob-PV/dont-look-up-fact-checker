/**
 * TypeScript types for dashboard statistics
 */

export interface OverviewStats {
  total_articles: number;
  total_claims: number;
  total_investigations: number;
  last_ingestion: string | null;
}

export interface VerdictDistribution {
  true: number;
  mostly_true: number;
  mixed: number;
  mostly_false: number;
  false: number;
  unverifiable: number;
}

export interface RecentActivity {
  time_range: string;
  new_articles: number;
  new_claims: number;
  new_investigations: number;
}

export interface QualityMetrics {
  avg_confidence: number;
  avg_propaganda_score: number;
  avg_source_reliability: number;
}

export interface ProcessingQueue {
  pending_articles: number;
  processing_articles: number;
  pending_claims: number;
  checking_claims: number;
}

export interface TrendingClaim {
  claim_text: string;
  verdict: string;
  confidence: number;
  article_count: number;
}

export interface PropagandaTechnique {
  technique: string;
  count: number;
}

export interface ProblematicSource {
  source_name: string;
  propaganda_score: number;
  article_count: number;
}

export interface PropagandaAnalysis {
  top_techniques: PropagandaTechnique[];
  problematic_sources: ProblematicSource[];
}

export interface DashboardStats {
  overview: OverviewStats;
  verdict_distribution: VerdictDistribution;
  recent_activity: RecentActivity;
  quality_metrics: QualityMetrics;
  processing_queue: ProcessingQueue;
  trending_claims: TrendingClaim[];
  propaganda_analysis: PropagandaAnalysis;
}
