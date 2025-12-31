import React, { useEffect } from 'react';
import { Investigation } from '../../types/investigation';

interface InvestigationDetailProps {
  investigation: Investigation;
  onClose: () => void;
}

const verdictLabels: Record<Investigation['verdict'], string> = {
  true: 'True',
  mostly_true: 'Mostly True',
  mixed: 'Mixed',
  mostly_false: 'Mostly False',
  false: 'False',
  unverifiable: 'Unverifiable',
};

export const InvestigationDetail: React.FC<InvestigationDetailProps> = ({
  investigation,
  onClose
}) => {
  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  // Prevent body scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={onClose}
      role="dialog"
      aria-labelledby="investigation-detail-title"
      aria-modal="true"
    >
      <div
        className="bg-white rounded-lg max-w-4xl max-h-[90vh] overflow-y-auto w-full"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center z-10">
          <h2 id="investigation-detail-title" className="text-2xl font-bold">
            Investigation Details
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-3xl leading-none"
            aria-label="Close investigation details"
          >
            ×
          </button>
        </div>

        <div className="p-6">
          {/* Claim */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-2">Claim</h3>
            <p className="text-gray-900">
              {investigation.claim?.claim_text || 'No claim text available'}
            </p>
          </div>

          {/* Verdict and Confidence */}
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">Verdict</h3>
              <p className="text-2xl font-bold capitalize">
                {verdictLabels[investigation.verdict]}
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Confidence Score</h3>
              <p className="text-2xl font-bold">
                {Math.round(investigation.confidence_score * 100)}%
              </p>
            </div>
          </div>

          {/* Summary */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-2">Summary</h3>
            <p className="text-gray-700">{investigation.summary}</p>
          </div>

          {/* Reasoning */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-2">Reasoning</h3>
            <p className="text-gray-700 whitespace-pre-line">
              {investigation.reasoning}
            </p>
          </div>

          {/* Evidence */}
          {investigation.evidence && investigation.evidence.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-4">
                Evidence ({investigation.evidence.length})
              </h3>

              <div className="space-y-4">
                {investigation.evidence.map((evidence) => (
                  <div
                    key={evidence.id}
                    className="border rounded-lg p-4 bg-gray-50"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <a
                          href={evidence.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary-700 hover:underline font-medium"
                          aria-label={`View source: ${evidence.source_name}`}
                        >
                          {evidence.source_name}
                        </a>
                      </div>

                      <span
                        className={`px-2 py-1 rounded text-xs font-semibold ${
                          evidence.stance === 'supporting'
                            ? 'bg-green-100 text-green-800'
                            : evidence.stance === 'refuting'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {evidence.stance}
                      </span>
                    </div>

                    <p className="text-gray-700 text-sm mb-2">
                      "{evidence.snippet}"
                    </p>

                    <div className="flex gap-4 text-xs text-gray-500">
                      <span>
                        Reliability: {Math.round(evidence.source_reliability * 100)}%
                      </span>
                      <span>
                        Relevance: {Math.round(evidence.relevance_score * 100)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Propaganda Signals */}
          {investigation.propaganda_signals?.techniques_detected?.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-4">
                Propaganda Techniques Detected
              </h3>

              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-sm text-yellow-800 mb-3">
                  Overall propaganda score:{' '}
                  <span className="font-semibold">
                    {Math.round(investigation.propaganda_signals.overall_propaganda_score * 100)}%
                  </span>
                </p>

                <div className="space-y-2">
                  {investigation.propaganda_signals.techniques_detected.map((technique, idx) => (
                    <div key={idx} className="text-sm">
                      <p className="font-medium text-yellow-900">
                        {technique.technique} ({Math.round(technique.confidence * 100)}%)
                      </p>
                      <p className="text-yellow-700 text-xs">
                        "{technique.evidence}"
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
