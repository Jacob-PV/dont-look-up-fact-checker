import React, { useState } from 'react';
import { useDashboardStats } from '../hooks/useDashboardStats';
import { StatCard } from '../components/dashboard/StatCard';
import { VerdictDistribution } from '../components/dashboard/VerdictDistribution';
import { RecentActivity } from '../components/dashboard/RecentActivity';
import { QualityMetrics } from '../components/dashboard/QualityMetrics';
import { TrendingClaims } from '../components/dashboard/TrendingClaims';
import { PropagandaAnalysis } from '../components/dashboard/PropagandaAnalysis';
import { ProcessingQueue } from '../components/dashboard/ProcessingQueue';
import { Loading } from '../components/common/Loading';
import { FileText, FileCheck, ClipboardCheck, RefreshCw } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

const DashboardPage: React.FC = () => {
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d'>('24h');
  const { data, isLoading, error, dataUpdatedAt } = useDashboardStats(timeRange);

  if (isLoading) return <Loading />;

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Error loading dashboard. Please try again.</p>
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <h1 className="text-4xl font-bold">Analytics Dashboard</h1>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <RefreshCw className="w-4 h-4" />
            <span>Updated {formatDistanceToNow(dataUpdatedAt, { addSuffix: true })}</span>
          </div>
        </div>
        <p className="text-gray-600">Real-time insights into fact-checking operations</p>
      </div>

      {/* Time Range Filter */}
      <div className="mb-6">
        <div className="inline-flex bg-white rounded-lg shadow-md p-1">
          {(['24h', '7d', '30d'] as const).map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                timeRange === range
                  ? 'bg-primary-700 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              {range === '24h' ? 'Last 24 Hours' : range === '7d' ? 'Last 7 Days' : 'Last 30 Days'}
            </button>
          ))}
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Articles"
          value={data.overview.total_articles}
          icon={FileText}
          color="blue"
        />
        <StatCard
          title="Total Claims"
          value={data.overview.total_claims}
          icon={FileCheck}
          color="green"
        />
        <StatCard
          title="Total Investigations"
          value={data.overview.total_investigations}
          icon={ClipboardCheck}
          color="yellow"
        />
        <StatCard
          title="Last Ingestion"
          value={
            data.overview.last_ingestion
              ? formatDistanceToNow(new Date(data.overview.last_ingestion), { addSuffix: true })
              : 'Never'
          }
          icon={RefreshCw}
          color="gray"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <VerdictDistribution distribution={data.verdict_distribution} />
        <RecentActivity activity={data.recent_activity} />
      </div>

      {/* Metrics and Queue */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <QualityMetrics metrics={data.quality_metrics} />
        <ProcessingQueue queue={data.processing_queue} />
      </div>

      {/* Trending and Propaganda */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TrendingClaims claims={data.trending_claims} />
        <PropagandaAnalysis analysis={data.propaganda_analysis} />
      </div>
    </div>
  );
};

export default DashboardPage;
