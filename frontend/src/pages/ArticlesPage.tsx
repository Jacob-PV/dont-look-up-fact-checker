import React from 'react';
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
