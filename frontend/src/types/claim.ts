export interface Claim {
  id: string;
  claim_text: string;
  claim_type?: string;
  context?: string;
  is_checkable: boolean;
  extraction_confidence?: number;
  status: string;
  investigation?: any;
  created_at: string;
}

export type Verdict = 'true' | 'mostly_true' | 'mixed' | 'mostly_false' | 'false' | 'unverifiable';
