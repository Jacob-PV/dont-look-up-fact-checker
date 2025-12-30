import apiClient from './client';

export const getArticles = async (params: any) => {
  const { data } = await apiClient.get('/articles', { params });
  return data;
};

export const getArticle = async (id: string) => {
  const { data } = await apiClient.get(`/articles/${id}`);
  return data;
};
