/**
 * QualityMetrics component - Display average quality scores
 */
import React from 'react';
import { QualityMetrics as QualityMetricsType } from '../../types/stats';

interface Props {
  metrics: QualityMetricsType;
}

export const QualityMetrics: React.FC<Props> = ({ metrics }) => {
  const getColorClass = (value: number, inverse: boolean = false) => {
    if (inverse) {
      if (value < 0.3) return 'bg-green-500';
      if (value < 0.6) return 'bg-yellow-500';
      return 'bg-red-500';
    } else {
      if (value >= 0.7) return 'bg-green-500';
      if (value >= 0.4) return 'bg-yellow-500';
      return 'bg-red-500';
    }
  };

  const metricsData = [
    {
      label: 'Avg Confidence',
      value: metrics.avg_confidence,
      percentage: metrics.avg_confidence * 100,
      inverse: false
    },
    {
      label: 'Avg Source Reliability',
      value: metrics.avg_source_reliability,
      percentage: metrics.avg_source_reliability * 100,
      inverse: false
    },
    {
      label: 'Avg Propaganda Score',
      value: metrics.avg_propaganda_score,
      percentage: metrics.avg_propaganda_score * 100,
      inverse: true
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Quality Metrics</h2>
      <div className="space-y-4">
        {metricsData.map((metric) => (
          <div key={metric.label}>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700">{metric.label}</span>
              <span className="text-sm font-medium text-gray-900">
                {metric.percentage.toFixed(0)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${getColorClass(metric.value, metric.inverse)}`}
                style={{ width: `${metric.percentage}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
