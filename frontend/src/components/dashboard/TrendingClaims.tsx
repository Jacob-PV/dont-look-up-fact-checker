/**
 * TrendingClaims component - List of trending claims
 */
import React, { useState } from 'react';
import { TrendingClaim } from '../../types/stats';
import { TrendingUp } from 'lucide-react';

interface Props {
  claims: TrendingClaim[];
}

const VERDICT_COLORS: Record<string, string> = {
  true: 'bg-green-100 text-green-800',
  mostly_true: 'bg-lime-100 text-lime-800',
  mixed: 'bg-yellow-100 text-yellow-800',
  mostly_false: 'bg-orange-100 text-orange-800',
  false: 'bg-red-100 text-red-800',
  unverifiable: 'bg-gray-100 text-gray-800'
};

export const TrendingClaims: React.FC<Props> = ({ claims }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const truncate = (text: string, maxLength: number = 100) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp className="w-5 h-5 text-primary-700" />
        <h2 className="text-xl font-semibold">Trending Claims</h2>
      </div>
      {claims.length > 0 ? (
        <div className="space-y-3">
          {claims.map((claim, index) => (
            <div
              key={index}
              className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer"
              onClick={() => setExpandedIndex(expandedIndex === index ? null : index)}
            >
              <div className="flex items-start justify-between gap-3 mb-2">
                <p className="text-sm text-gray-900 flex-1">
                  {expandedIndex === index
                    ? claim.claim_text
                    : truncate(claim.claim_text)}
                </p>
                <span className={`px-2 py-1 rounded text-xs font-medium whitespace-nowrap ${VERDICT_COLORS[claim.verdict] || 'bg-gray-100 text-gray-800'}`}>
                  {claim.verdict.replace('_', ' ')}
                </span>
              </div>
              <div className="flex gap-4 text-xs text-gray-600">
                <span>Confidence: {(claim.confidence * 100).toFixed(0)}%</span>
                <span>Articles: {claim.article_count}</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-gray-500 text-center py-8">No trending claims yet</p>
      )}
    </div>
  );
};
