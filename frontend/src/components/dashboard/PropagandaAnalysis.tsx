/**
 * PropagandaAnalysis component - Show propaganda techniques and problematic sources
 */
import React from 'react';
import { PropagandaAnalysis as PropagandaAnalysisType } from '../../types/stats';
import { AlertTriangle } from 'lucide-react';

interface Props {
  analysis: PropagandaAnalysisType;
}

export const PropagandaAnalysis: React.FC<Props> = ({ analysis }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle className="w-5 h-5 text-red-600" />
        <h2 className="text-xl font-semibold">Propaganda Analysis</h2>
      </div>

      {/* Top Techniques */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Top Techniques</h3>
        {analysis.top_techniques.length > 0 ? (
          <div className="space-y-2">
            {analysis.top_techniques.map((tech, index) => (
              <div key={index} className="flex items-center gap-3">
                <span className="text-sm text-gray-700 flex-1">{tech.technique}</span>
                <span className="text-sm font-medium text-gray-900">{tech.count}</span>
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-red-500 h-2 rounded-full"
                    style={{ width: `${(tech.count / analysis.top_techniques[0].count) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-sm">No techniques detected</p>
        )}
      </div>

      {/* Problematic Sources */}
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Problematic Sources</h3>
        {analysis.problematic_sources.length > 0 ? (
          <div className="space-y-2">
            {analysis.problematic_sources.map((source, index) => (
              <div key={index} className="flex items-center gap-3">
                <span className="text-sm text-gray-700 flex-1">{source.source_name}</span>
                <span className="text-xs text-gray-600">{source.article_count} articles</span>
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  source.propaganda_score >= 0.6 ? 'bg-red-100 text-red-800' :
                  source.propaganda_score >= 0.3 ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {(source.propaganda_score * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-sm">No problematic sources detected</p>
        )}
      </div>
    </div>
  );
};
