import { useQuery } from '@tanstack/react-query';
import { InvestigationsResponse, Investigation } from '../types/investigation';
import { getInvestigations, getInvestigation } from '../api/investigations';

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
    queryFn: () => getInvestigations({
      limit,
      offset,
      verdict,
      min_confidence: minConfidence
    }),
    staleTime: 30000, // 30 seconds
    refetchInterval: 60000, // Refetch every minute for real-time updates
  });
}

export function useInvestigation(id: string) {
  return useQuery<Investigation>({
    queryKey: ['investigation', id],
    queryFn: () => getInvestigation(id),
    enabled: !!id,
  });
}
