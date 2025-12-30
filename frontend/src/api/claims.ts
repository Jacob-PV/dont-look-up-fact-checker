import apiClient from './client';

export const getClaims = async (params: any) => {
  const { data } = await apiClient.get('/claims', { params });
  return data;
};

export const getClaim = async (id: string) => {
  const { data } = await apiClient.get(`/claims/${id}`);
  return data;
};
