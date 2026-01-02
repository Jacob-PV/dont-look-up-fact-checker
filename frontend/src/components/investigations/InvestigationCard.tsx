import React from 'react';
import { Investigation } from '../../types/investigation';

interface InvestigationCardProps {
  investigation: Investigation;
  onClick?: () => void;
}

const verdictColors: Record<Investigation['verdict'], string> = {
  true: 'bg-verdict-true text-white',
  mostly_true: 'bg-verdict-mostly_true text-white',
  mixed: 'bg-verdict-mixed text-white',
  mostly_false: 'bg-verdict-mostly_false text-white',
  false: 'bg-verdict-false text-white',
  unverifiable: 'bg-verdict-unverifiable text-white',
};

const verdictLabels: Record<Investigation['verdict'], string> = {
  true: 'True',
  mostly_true: 'Mostly True',
  mixed: 'Mixed',
  mostly_false: 'Mostly False',
  false: 'False',
  unverifiable: 'Unverifiable',
};

export const InvestigationCard: React.FC<InvestigationCardProps> = ({
  investigation,
  onClick
}) => {
  const verdictColor = verdictColors[investigation.verdict];
  const verdictLabel = verdictLabels[investigation.verdict];

  return (
    <div
      className="bg-white rounded-lg shadow-md p-6 hover:shadow-hover transition-shadow cursor-pointer"
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyPress={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          onClick?.();
        }
      }}
      aria-label={`Investigation: ${investigation.claim_text || 'Unknown claim'}. Verdict: ${verdictLabel}. Confidence: ${Math.round(investigation.confidence_score * 100)}%`}
    >
      {/* Status Badge */}
      {investigation.status === 'in_progress' && (
        <div className="mb-3">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            In Progress
          </span>
        </div>
      )}

      {/* Verdict Badge */}
      <div className="mb-3">
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold ${verdictColor}`}>
          {verdictLabel}
        </span>
      </div>

      {/* Claim Text */}
      <p className="text-gray-900 font-medium mb-3 line-clamp-3">
        {investigation.claim_text || 'No claim text available'}
      </p>

      {/* Summary */}
      <p className="text-gray-600 text-sm mb-4 line-clamp-2">
        {investigation.summary}
      </p>

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        {/* Confidence Score */}
        <div>
          <p className="text-xs text-gray-500 mb-1">Confidence</p>
          <div className="flex items-center">
            <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
              <div
                className="bg-primary-500 h-2 rounded-full transition-all"
                style={{ width: `${investigation.confidence_score * 100}%` }}
              />
            </div>
            <span className="text-sm font-semibold">
              {Math.round(investigation.confidence_score * 100)}%
            </span>
          </div>
        </div>

        {/* Evidence Count */}
        <div>
          <p className="text-xs text-gray-500 mb-1">Evidence</p>
          <p className="text-sm">
            <span className="text-green-600 font-semibold">
              {investigation.supporting_evidence_count}
            </span>
            {' / '}
            <span className="text-red-600 font-semibold">
              {investigation.refuting_evidence_count}
            </span>
            <span className="text-gray-500 text-xs ml-1">
              (of {investigation.evidence_count})
            </span>
          </p>
        </div>
      </div>

      {/* Propaganda Alert */}
      {investigation.propaganda_signals?.overall_propaganda_score > 0.5 && (
        <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded">
          <p className="text-xs text-yellow-800">
            <span className="font-semibold">⚠ Propaganda Detected:</span>
            {' '}
            {Math.round(investigation.propaganda_signals.overall_propaganda_score * 100)}% confidence
          </p>
        </div>
      )}

      {/* Timestamp */}
      <p className="text-xs text-gray-400 mt-3">
        {new Date(investigation.created_at).toLocaleDateString()}
      </p>
    </div>
  );
};
