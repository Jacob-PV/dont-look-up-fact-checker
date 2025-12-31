import { useQuery } from '@tanstack/react-query';
import { InvestigationsResponse, Investigation } from '../types/investigation';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

interface UseInvestigationsParams {
  limit?: number;
  offset?: number;
  verdict?: string;
  minConfidence?: number;
}

export function useInvestigations(params: UseInvestigationsParams = {}) {
  const {
    limit = 20,
    offset = 0,
    verdict,
    minConfidence
  } = params;

  return useQuery<InvestigationsResponse>({
    queryKey: ['investigations', limit, offset, verdict, minConfidence],
    queryFn: async () => {
      const searchParams = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString(),
      });

      if (verdict) {
        searchParams.append('verdict', verdict);
      }

      if (minConfidence !== undefined) {
        searchParams.append('min_confidence', minConfidence.toString());
      }

      const response = await fetch(`${API_URL}/investigations?${searchParams}`);

      if (!response.ok) {
        throw new Error('Failed to fetch investigations');
      }

      return response.json();
    },
    staleTime: 30000, // 30 seconds
    refetchInterval: 60000, // Refetch every minute for real-time updates
  });
}

export function useInvestigation(id: string) {
  return useQuery<Investigation>({
    queryKey: ['investigation', id],
    queryFn: async () => {
      const response = await fetch(`${API_URL}/investigations/${id}`);

      if (!response.ok) {
        throw new Error('Failed to fetch investigation');
      }

      return response.json();
    },
    enabled: !!id,
  });
}
