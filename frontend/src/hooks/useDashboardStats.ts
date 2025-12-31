/**
 * React Query hook for fetching dashboard statistics
 */
import { useQuery } from '@tanstack/react-query';
import { getDashboardStats } from '../api/client';
import { DashboardStats } from '../types/stats';

/**
 * Hook to fetch and cache dashboard statistics
 * @param timeRange - Time range for recent activity ('24h', '7d', '30d')
 * @returns React Query result with dashboard statistics
 */
export function useDashboardStats(timeRange: string = '24h') {
  return useQuery<DashboardStats>({
    queryKey: ['dashboardStats', timeRange],
    queryFn: () => getDashboardStats(timeRange),
    refetchInterval: 60000, // Auto-refresh every 60 seconds
    staleTime: 30000, // Consider stale after 30 seconds
  });
}
