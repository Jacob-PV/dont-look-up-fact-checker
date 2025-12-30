import { useQuery } from '@tanstack/react-query';
import { getClaims } from '../api/claims';

export function useClaims(params: any = {}) {
  return useQuery({
    queryKey: ['claims', params],
    queryFn: () => getClaims(params),
  });
}
