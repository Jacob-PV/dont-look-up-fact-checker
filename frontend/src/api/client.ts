import axios from 'axios';
import { DashboardStats } from '../types/stats';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;

/**
 * Fetch dashboard statistics
 * @param timeRange - Time range for recent activity ('24h', '7d', '30d')
 * @returns Dashboard statistics
 */
export async function getDashboardStats(timeRange: string = '24h'): Promise<DashboardStats> {
  const response = await apiClient.get(`/stats/overview?time_range=${timeRange}`);
  return response.data;
}
