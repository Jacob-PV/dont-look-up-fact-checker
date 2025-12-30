import apiClient from './client';

export const getInvestigations = async (params: any) => {
  const { data } = await apiClient.get('/investigations', { params });
  return data;
};

export const getInvestigation = async (id: string) => {
  const { data } = await apiClient.get(`/investigations/${id}`);
  return data;
};
