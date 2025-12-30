import { useQuery } from '@tanstack/react-query';
import { getArticles } from '../api/articles';

export function useArticles(params: any = {}) {
  return useQuery({
    queryKey: ['articles', params],
    queryFn: () => getArticles(params),
  });
}
