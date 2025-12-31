import React, { useState } from 'react';
import { useInvestigations } from '../hooks/useInvestigations';
import { InvestigationCard } from '../components/investigations/InvestigationCard';
import { InvestigationDetail } from '../components/investigations/InvestigationDetail';
import { Loading } from '../components/common/Loading';
import { Investigation } from '../types/investigation';

const InvestigationsPage: React.FC = () => {
  const [selectedInvestigation, setSelectedInvestigation] = useState<Investigation | null>(null);
  const [verdict, setVerdict] = useState<string>('');
  const [minConfidence, setMinConfidence] = useState<number>(0);
  const [page, setPage] = useState<number>(0);

  const limit = 20;
  const offset = page * limit;

  const { data, isLoading, error } = useInvestigations({
    limit,
    offset,
    verdict: verdict || undefined,
    minConfidence: minConfidence > 0 ? minConfidence : undefined,
  });

  if (isLoading) return <Loading />;

  if (error) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Error loading investigations. Please try again.</p>
        </div>
      </div>
    );
  }

  const totalPages = data ? Math.ceil(data.total / limit) : 0;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Investigations</h1>
        <p className="text-gray-600">
          {data?.total || 0} fact-check investigations completed
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Filter Results</h2>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Verdict Filter */}
          <div>
            <label
              htmlFor="verdict-filter"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Verdict Type
            </label>
            <select
              id="verdict-filter"
              value={verdict}
              onChange={(e) => {
                setVerdict(e.target.value);
                setPage(0);
              }}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              aria-label="Filter investigations by verdict type"
            >
              <option value="">All Verdicts</option>
              <option value="true">True</option>
              <option value="mostly_true">Mostly True</option>
              <option value="mixed">Mixed</option>
              <option value="mostly_false">Mostly False</option>
              <option value="false">False</option>
              <option value="unverifiable">Unverifiable</option>
            </select>
          </div>

          {/* Confidence Filter */}
          <div>
            <label
              htmlFor="confidence-filter"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Minimum Confidence: {Math.round(minConfidence * 100)}%
            </label>
            <input
              id="confidence-filter"
              type="range"
              min="0"
              max="100"
              value={minConfidence * 100}
              onChange={(e) => {
                setMinConfidence(parseInt(e.target.value) / 100);
                setPage(0);
              }}
              className="w-full"
              aria-label={`Filter investigations by minimum confidence score: ${Math.round(minConfidence * 100)}%`}
            />
          </div>
        </div>

        {/* Active Filters Display */}
        {(verdict || minConfidence > 0) && (
          <div className="mt-4 flex gap-2 flex-wrap">
            {verdict && (
              <span className="inline-flex items-center px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm">
                Verdict: {verdict}
                <button
                  onClick={() => {
                    setVerdict('');
                    setPage(0);
                  }}
                  className="ml-2 text-primary-600 hover:text-primary-800"
                  aria-label="Clear verdict filter"
                >
                  ×
                </button>
              </span>
            )}
            {minConfidence > 0 && (
              <span className="inline-flex items-center px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm">
                Min Confidence: {Math.round(minConfidence * 100)}%
                <button
                  onClick={() => {
                    setMinConfidence(0);
                    setPage(0);
                  }}
                  className="ml-2 text-primary-600 hover:text-primary-800"
                  aria-label="Clear confidence filter"
                >
                  ×
                </button>
              </span>
            )}
            <button
              onClick={() => {
                setVerdict('');
                setMinConfidence(0);
                setPage(0);
              }}
              className="text-primary-700 hover:text-primary-900 text-sm font-medium"
            >
              Clear all filters
            </button>
          </div>
        )}
      </div>

      {/* Investigation Grid */}
      {data?.items && data.items.length > 0 ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {data.items.map((investigation) => (
            <InvestigationCard
              key={investigation.id}
              investigation={investigation}
              onClick={() => setSelectedInvestigation(investigation)}
            />
          ))}
        </div>
      ) : (
        /* Empty State */
        <div className="text-center py-12">
          <div className="mb-4">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
              />
            </svg>
          </div>
          <p className="text-gray-600 mb-2">
            {verdict || minConfidence > 0
              ? 'No investigations match your filters'
              : 'No investigations completed yet'}
          </p>
          <p className="text-gray-500 text-sm">
            {verdict || minConfidence > 0
              ? 'Try adjusting your filters to see more results'
              : 'Investigations will appear here as claims are fact-checked'}
          </p>
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-4" role="navigation" aria-label="Pagination">
          <button
            onClick={() => setPage(page - 1)}
            disabled={page === 0}
            className="px-4 py-2 bg-primary-700 text-white rounded-md disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-primary-500 transition-colors"
            aria-label="Previous page of investigations"
          >
            Previous
          </button>

          <span className="text-gray-700" aria-live="polite">
            Page {page + 1} of {totalPages}
          </span>

          <button
            onClick={() => setPage(page + 1)}
            disabled={page >= totalPages - 1}
            className="px-4 py-2 bg-primary-700 text-white rounded-md disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-primary-500 transition-colors"
            aria-label="Next page of investigations"
          >
            Next
          </button>
        </div>
      )}

      {/* Detail Modal */}
      {selectedInvestigation && (
        <InvestigationDetail
          investigation={selectedInvestigation}
          onClose={() => setSelectedInvestigation(null)}
        />
      )}
    </div>
  );
};

export default InvestigationsPage;
