#!/usr/bin/env python3
"""Generate all frontend React components."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent / "frontend" / "src"

FRONTEND_FILES = {
    # API CLIENT
    "api/client.ts": '''import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
''',

    "api/articles.ts": '''import apiClient from './client';

export const getArticles = async (params: any) => {
  const { data } = await apiClient.get('/articles', { params });
  return data;
};

export const getArticle = async (id: string) => {
  const { data } = await apiClient.get(`/articles/${id}`);
  return data;
};
''',

    "api/claims.ts": '''import apiClient from './client';

export const getClaims = async (params: any) => {
  const { data } = await apiClient.get('/claims', { params });
  return data;
};

export const getClaim = async (id: string) => {
  const { data } = await apiClient.get(`/claims/${id}`);
  return data;
};
''',

    "api/investigations.ts": '''import apiClient from './client';

export const getInvestigations = async (params: any) => {
  const { data } = await apiClient.get('/investigations', { params });
  return data;
};

export const getInvestigation = async (id: string) => {
  const { data } = await apiClient.get(`/investigations/${id}`);
  return data;
};
''',

    # TYPES
    "types/common.ts": '''export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}
''',

    "types/article.ts": '''export interface Article {
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
''',

    "types/claim.ts": '''export interface Claim {
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
''',

    # HOOKS
    "hooks/useArticles.ts": '''import { useQuery } from '@tanstack/react-query';
import { getArticles } from '../api/articles';

export function useArticles(params: any = {}) {
  return useQuery({
    queryKey: ['articles', params],
    queryFn: () => getArticles(params),
  });
}
''',

    "hooks/useClaims.ts": '''import { useQuery } from '@tanstack/react-query';
import { getClaims } from '../api/claims';

export function useClaims(params: any = {}) {
  return useQuery({
    queryKey: ['claims', params],
    queryFn: () => getClaims(params),
  });
}
''',

    # COMPONENTS - Common
    "components/common/Button.tsx": '''import React from 'react';
import clsx from 'clsx';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ variant = 'primary', children, className, ...props }) => {
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    ghost: 'hover:bg-gray-100',
  };

  return (
    <button className={clsx('btn', variants[variant], className)} {...props}>
      {children}
    </button>
  );
};
''',

    "components/common/Card.tsx": '''import React from 'react';
import clsx from 'clsx';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, className, onClick }) => {
  return (
    <div className={clsx('card', onClick && 'cursor-pointer', className)} onClick={onClick}>
      {children}
    </div>
  );
};
''',

    "components/common/Badge.tsx": '''import React from 'react';
import clsx from 'clsx';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'danger';
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = 'default' }) => {
  const variants = {
    default: 'bg-gray-200 text-gray-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    danger: 'bg-red-100 text-red-800',
  };

  return <span className={clsx('badge', variants[variant])}>{children}</span>;
};
''',

    "components/common/Loading.tsx": '''import React from 'react';

export const Loading: React.FC = () => {
  return (
    <div className="flex justify-center items-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-700"></div>
    </div>
  );
};
''',

    "components/common/ConfidenceMeter.tsx": '''import React from 'react';

interface ConfidenceMeterProps {
  confidence: number; // 0 to 1
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({ confidence }) => {
  const percentage = Math.round(confidence * 100);

  const getColor = () => {
    if (confidence >= 0.8) return 'bg-green-500';
    if (confidence >= 0.6) return 'bg-yellow-500';
    return 'bg-orange-500';
  };

  return (
    <div className="w-full">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium">Confidence</span>
        <span className="text-sm font-medium">{percentage}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div
          className={`${getColor()} h-2.5 rounded-full transition-all`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
''',

    "components/claims/VerdictBadge.tsx": '''import React from 'react';
import { Verdict } from '../../types/claim';

interface VerdictBadgeProps {
  verdict: Verdict;
}

const verdictConfig = {
  true: { label: 'True', color: 'bg-verdict-true' },
  mostly_true: { label: 'Mostly True', color: 'bg-verdict-mostly_true' },
  mixed: { label: 'Mixed', color: 'bg-verdict-mixed' },
  mostly_false: { label: 'Mostly False', color: 'bg-verdict-mostly_false' },
  false: { label: 'False', color: 'bg-verdict-false' },
  unverifiable: { label: 'Unverifiable', color: 'bg-verdict-unverifiable' },
};

export const VerdictBadge: React.FC<VerdictBadgeProps> = ({ verdict }) => {
  const config = verdictConfig[verdict] || verdictConfig.unverifiable;

  return (
    <span className={`${config.color} text-white px-3 py-1 rounded-full text-sm font-semibold uppercase`}>
      {config.label}
    </span>
  );
};
''',

    "components/articles/ArticleCard.tsx": '''import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';
import { Article } from '../../types/article';
import { formatDistanceToNow } from 'date-fns';

interface ArticleCardProps {
  article: Article;
}

export const ArticleCard: React.FC<ArticleCardProps> = ({ article }) => {
  const navigate = useNavigate();

  const statusVariant = article.status === 'analyzed' ? 'success' : 'default';

  return (
    <Card onClick={() => navigate(`/articles/${article.id}`)}>
      <div className="flex items-center gap-2 mb-3">
        <span className="text-sm text-gray-600">{article.source_name}</span>
        <Badge variant={statusVariant}>{article.status}</Badge>
      </div>

      <h3 className="text-xl font-semibold mb-2 text-gray-900">{article.title}</h3>

      {article.author && (
        <p className="text-sm text-gray-500 mb-3">
          by {article.author}
        </p>
      )}

      {article.published_at && (
        <p className="text-sm text-gray-500 mb-3">
          {formatDistanceToNow(new Date(article.published_at), { addSuffix: true })}
        </p>
      )}

      <div className="flex justify-between items-center mt-4">
        <span className="text-sm text-gray-700">{article.claim_count} claims</span>
        <span className="text-primary-700 hover:underline">View Details →</span>
      </div>
    </Card>
  );
};
''',

    # PAGES
    "pages/Home.tsx": '''import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/common/Button';

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-6xl font-bold mb-4 text-primary-900">Don't Look Up</h1>
        <p className="text-2xl text-gray-700 mb-8">
          Automated AI-powered fact-checking with full transparency
        </p>

        <div className="flex gap-4 justify-center">
          <Button onClick={() => navigate('/articles')}>
            View Articles
          </Button>
          <Button variant="secondary" onClick={() => navigate('/about')}>
            Learn More
          </Button>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="card text-center">
          <h3 className="text-xl font-semibold mb-2">Automated Ingestion</h3>
          <p className="text-gray-600">
            Automatically fetches and analyzes articles from trusted news sources
          </p>
        </div>

        <div className="card text-center">
          <h3 className="text-xl font-semibold mb-2">AI-Powered Analysis</h3>
          <p className="text-gray-600">
            Uses LLMs to extract claims and search for evidence
          </p>
        </div>

        <div className="card text-center">
          <h3 className="text-xl font-semibold mb-2">Full Transparency</h3>
          <p className="text-gray-600">
            Shows confidence scores, evidence, and reasoning for all verdicts
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
''',

    "pages/ArticlesPage.tsx": '''import React from 'react';
import { useArticles } from '../hooks/useArticles';
import { ArticleCard } from '../components/articles/ArticleCard';
import { Loading } from '../components/common/Loading';

const ArticlesPage: React.FC = () => {
  const { data, isLoading, error } = useArticles();

  if (isLoading) return <Loading />;
  if (error) return <div>Error loading articles</div>;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Articles</h1>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data?.items?.map((article: any) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>

      {data?.items?.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600">No articles found</p>
        </div>
      )}
    </div>
  );
};

export default ArticlesPage;
''',

    "pages/ArticleDetailPage.tsx": '''import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getArticle } from '../api/articles';
import { Loading } from '../components/common/Loading';
import { Badge } from '../components/common/Badge';

const ArticleDetailPage: React.FC = () => {
  const { articleId } = useParams<{ articleId: string }>();

  const { data: article, isLoading } = useQuery({
    queryKey: ['article', articleId],
    queryFn: () => getArticle(articleId!),
    enabled: !!articleId,
  });

  if (isLoading) return <Loading />;
  if (!article) return <div>Article not found</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="card mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Badge>{article.source_name}</Badge>
          <Badge variant={article.status === 'analyzed' ? 'success' : 'default'}>
            {article.status}
          </Badge>
        </div>

        <h1 className="text-3xl font-bold mb-4">{article.title}</h1>

        {article.author && (
          <p className="text-gray-600 mb-2">by {article.author}</p>
        )}

        {article.url && (
          <a href={article.url} target="_blank" rel="noopener noreferrer" className="text-primary-700 hover:underline">
            View original article →
          </a>
        )}
      </div>

      <div className="card">
        <h2 className="text-2xl font-bold mb-4">Extracted Claims</h2>

        {article.claims?.length === 0 && (
          <p className="text-gray-600">No claims extracted yet</p>
        )}

        <div className="space-y-4">
          {article.claims?.map((claim: any) => (
            <div key={claim.id} className="border-l-4 border-primary-500 pl-4 py-2">
              <p className="text-gray-900">{claim.claim_text}</p>
              <Badge variant="default">{claim.status}</Badge>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ArticleDetailPage;
''',

    "pages/ClaimDetailPage.tsx": '''import React from 'react';

const ClaimDetailPage: React.FC = () => {
  return <div className="max-w-4xl mx-auto px-4 py-8">
    <h1>Claim Detail</h1>
    <p>Claim detail page coming soon</p>
  </div>;
};

export default ClaimDetailPage;
''',

    "pages/InvestigationsPage.tsx": '''import React from 'react';

const InvestigationsPage: React.FC = () => {
  return <div className="max-w-6xl mx-auto px-4 py-8">
    <h1>Investigations</h1>
    <p>Investigations page coming soon</p>
  </div>;
};

export default InvestigationsPage;
''',

    "pages/DashboardPage.tsx": '''import React from 'react';

const DashboardPage: React.FC = () => {
  return <div className="max-w-6xl mx-auto px-4 py-8">
    <h1>Dashboard</h1>
    <p>Dashboard page coming soon</p>
  </div>;
};

export default DashboardPage;
''',

    "pages/AboutPage.tsx": '''import React from 'react';

const AboutPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6">About Don't Look Up</h1>

      <div className="prose max-w-none">
        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Our Mission</h2>
          <p className="text-gray-700 mb-4">
            Don't Look Up is an automated fact-checking platform that uses AI to verify claims
            in news articles with full transparency. Our goal is to help people navigate the
            information landscape with confidence.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">How It Works</h2>
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li>We automatically ingest articles from trusted news sources</li>
            <li>AI extracts verifiable factual claims from each article</li>
            <li>Our system searches for supporting and refuting evidence</li>
            <li>Claims are analyzed and assigned a verdict with confidence score</li>
            <li>All evidence and reasoning is shown transparently to users</li>
          </ol>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Privacy & Transparency</h2>
          <p className="text-gray-700 mb-4">
            We take privacy seriously. All personal information is automatically detected
            and redacted before storage. Our fact-checking process is fully transparent -
            we show you the evidence, sources, and reasoning behind every verdict.
          </p>
        </section>
      </div>
    </div>
  );
};

export default AboutPage;
''',

    "pages/NotFoundPage.tsx": '''import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/common/Button';

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="max-w-2xl mx-auto px-4 py-16 text-center">
      <h1 className="text-6xl font-bold mb-4">404</h1>
      <p className="text-2xl text-gray-700 mb-8">Page not found</p>
      <Button onClick={() => navigate('/')}>Go Home</Button>
    </div>
  );
};

export default NotFoundPage;
''',

    # LAYOUT
    "components/layout/Layout.tsx": '''import React from 'react';
import Header from './Header';
import Footer from './Footer';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
''',

    "components/layout/Header.tsx": '''import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Header: React.FC = () => {
  const navigate = useNavigate();

  return (
    <header className="bg-primary-900 text-white sticky top-0 z-50 shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="text-2xl font-bold font-heading">
            Don't Look Up
          </Link>

          <nav className="flex gap-6">
            <Link to="/" className="hover:text-primary-300 transition">
              Home
            </Link>
            <Link to="/articles" className="hover:text-primary-300 transition">
              Articles
            </Link>
            <Link to="/investigations" className="hover:text-primary-300 transition">
              Investigations
            </Link>
            <Link to="/dashboard" className="hover:text-primary-300 transition">
              Dashboard
            </Link>
            <Link to="/about" className="hover:text-primary-300 transition">
              About
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
''',

    "components/layout/Footer.tsx": '''import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-100 py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 text-center text-gray-600">
        <p>© 2025 Don't Look Up - Automated Fact-Checking</p>
        <p className="text-sm mt-2">Built with transparency. Powered by AI.</p>
      </div>
    </footer>
  );
};

export default Footer;
''',
}

def create_frontend_files():
    """Create all frontend files."""
    for file_path, content in FRONTEND_FILES.items():
        full_path = BASE_DIR / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Creating: {file_path}")
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"\nCreated {len(FRONTEND_FILES)} frontend files successfully!")

if __name__ == "__main__":
    create_frontend_files()
