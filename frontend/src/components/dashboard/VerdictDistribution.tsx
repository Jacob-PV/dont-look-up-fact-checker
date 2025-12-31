/**
 * VerdictDistribution component - Pie chart showing verdict breakdown
 */
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { VerdictDistribution as VerdictDistributionType } from '../../types/stats';

interface Props {
  distribution: VerdictDistributionType;
}

const VERDICT_COLORS: Record<string, string> = {
  true: '#059669',
  mostly_true: '#84CC16',
  mixed: '#F59E0B',
  mostly_false: '#F97316',
  false: '#DC2626',
  unverifiable: '#6B7280'
};

const VERDICT_LABELS: Record<string, string> = {
  true: 'True',
  mostly_true: 'Mostly True',
  mixed: 'Mixed',
  mostly_false: 'Mostly False',
  false: 'False',
  unverifiable: 'Unverifiable'
};

export const VerdictDistribution: React.FC<Props> = ({ distribution }) => {
  const data = Object.entries(distribution)
    .map(([key, value]) => ({
      name: VERDICT_LABELS[key as keyof typeof VERDICT_LABELS],
      value: value,
      color: VERDICT_COLORS[key as keyof typeof VERDICT_COLORS]
    }))
    .filter(item => item.value > 0);

  const total = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Verdict Distribution</h2>
      {total > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={80}
              label={(entry) => `${((entry.value / total) * 100).toFixed(0)}%`}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      ) : (
        <p className="text-gray-500 text-center py-12">No investigations yet</p>
      )}
    </div>
  );
};
