export interface Article {
  id: string;
  title: string;
  url: string;
  author?: string;
  published_at?: string;
  source_name?: string;
  status: string;
  claim_count: number;
  created_at: string;
}

export interface ArticleDetail extends Article {
  content?: string;
  claims: any[];
}
