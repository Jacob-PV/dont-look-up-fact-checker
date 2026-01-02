import React, { useState } from 'react';
import { useArticles } from '../hooks/useArticles';
import { ArticleCard } from '../components/articles/ArticleCard';
import { Loading } from '../components/common/Loading';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const ITEMS_PER_PAGE = 20;

const ArticlesPage: React.FC = () => {
  const [currentPage, setCurrentPage] = useState(1);

  const offset = (currentPage - 1) * ITEMS_PER_PAGE;
  const { data, isLoading, error } = useArticles({
    limit: ITEMS_PER_PAGE,
    offset
  });

  const totalPages = data?.total ? Math.ceil(data.total / ITEMS_PER_PAGE) : 0;
  const startItem = data?.total ? offset + 1 : 0;
  const endItem = data?.total ? Math.min(offset + ITEMS_PER_PAGE, data.total) : 0;

  const handlePreviousPage = () => {
    setCurrentPage(prev => Math.max(1, prev - 1));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleNextPage = () => {
    setCurrentPage(prev => Math.min(totalPages, prev + 1));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (isLoading) return <Loading />;
  if (error) return <div>Error loading articles</div>;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-4xl font-bold">Articles</h1>
        {data?.total && (
          <p className="text-gray-600">
            Showing {startItem}-{endItem} of {data.total} articles
          </p>
        )}
      </div>

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

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4 mt-8">
          <button
            onClick={handlePreviousPage}
            disabled={currentPage === 1}
            className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-white"
          >
            <ChevronLeft className="w-4 h-4" />
            Previous
          </button>

          <span className="text-gray-700">
            Page {currentPage} of {totalPages}
          </span>

          <button
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
            className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-white"
          >
            Next
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
};

export default ArticlesPage;
