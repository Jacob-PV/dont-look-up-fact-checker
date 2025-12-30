import React from 'react';
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
