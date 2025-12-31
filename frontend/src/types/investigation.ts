export interface Investigation {
  id: string;
  claim_id: string;
  verdict: 'true' | 'mostly_true' | 'mixed' | 'mostly_false' | 'false' | 'unverifiable';
  confidence_score: number;
  summary: string;
  reasoning: string;
  propaganda_signals: PropagandaSignals;
  source_reliability_avg: number;
  evidence_count: number;
  supporting_evidence_count: number;
  refuting_evidence_count: number;
  status: 'in_progress' | 'completed' | 'error';
  created_at: string;
  updated_at: string;
  claim?: Claim;
  evidence?: Evidence[];
}

export interface Evidence {
  id: string;
  investigation_id: string;
  source_url: string;
  source_name: string;
  source_reliability: number;
  snippet: string;
  context: string;
  stance: 'supporting' | 'refuting' | 'neutral';
  relevance_score: number;
  published_at?: string;
  created_at: string;
}

export interface PropagandaSignals {
  techniques_detected: PropagandaTechnique[];
  overall_propaganda_score: number;
}

export interface PropagandaTechnique {
  technique: string;
  confidence: number;
  evidence: string;
}

export interface Claim {
  id: string;
  article_id: string;
  claim_text: string;
  claim_type: string;
  context: string;
  is_checkable: boolean;
  extraction_confidence: number;
  status: string;
  created_at: string;
}

export interface InvestigationsResponse {
  items: Investigation[];
  total: number;
  limit: number;
  offset: number;
}
