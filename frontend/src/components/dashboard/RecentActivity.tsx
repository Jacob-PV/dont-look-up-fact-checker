/**
 * RecentActivity component - Bar chart showing recent activity
 */
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { RecentActivity as RecentActivityType } from '../../types/stats';

interface Props {
  activity: RecentActivityType;
}

export const RecentActivity: React.FC<Props> = ({ activity }) => {
  const data = [
    { name: 'Articles', value: activity.new_articles, fill: '#3b82f6' },
    { name: 'Claims', value: activity.new_claims, fill: '#10b981' },
    { name: 'Investigations', value: activity.new_investigations, fill: '#f59e0b' }
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-2">Recent Activity</h2>
      <p className="text-sm text-gray-600 mb-4">Last {activity.time_range}</p>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
