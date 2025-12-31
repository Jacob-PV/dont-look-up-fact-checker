/**
 * ProcessingQueue component - Show pipeline status
 */
import React from 'react';
import { ProcessingQueue as ProcessingQueueType } from '../../types/stats';
import { Clock, Loader } from 'lucide-react';

interface Props {
  queue: ProcessingQueueType;
}

export const ProcessingQueue: React.FC<Props> = ({ queue }) => {
  const queueItems = [
    { label: 'Pending Articles', count: queue.pending_articles, icon: Clock, color: 'text-gray-600' },
    { label: 'Processing Articles', count: queue.processing_articles, icon: Loader, color: 'text-blue-600' },
    { label: 'Pending Claims', count: queue.pending_claims, icon: Clock, color: 'text-gray-600' },
    { label: 'Checking Claims', count: queue.checking_claims, icon: Loader, color: 'text-blue-600' }
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Processing Queue</h2>
      <div className="grid grid-cols-2 gap-4">
        {queueItems.map((item) => (
          <div key={item.label} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <item.icon className={`w-5 h-5 ${item.color}`} />
            <div>
              <p className="text-xs text-gray-600">{item.label}</p>
              <p className="text-xl font-bold text-gray-900">{item.count}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
