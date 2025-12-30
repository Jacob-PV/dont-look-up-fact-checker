import React from 'react';
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
