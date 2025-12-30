import React from 'react';
import { Verdict } from '../../types/claim';

interface VerdictBadgeProps {
  verdict: Verdict;
}

const verdictConfig = {
  true: { label: 'True', color: 'bg-verdict-true' },
  mostly_true: { label: 'Mostly True', color: 'bg-verdict-mostly_true' },
  mixed: { label: 'Mixed', color: 'bg-verdict-mixed' },
  mostly_false: { label: 'Mostly False', color: 'bg-verdict-mostly_false' },
  false: { label: 'False', color: 'bg-verdict-false' },
  unverifiable: { label: 'Unverifiable', color: 'bg-verdict-unverifiable' },
};

export const VerdictBadge: React.FC<VerdictBadgeProps> = ({ verdict }) => {
  const config = verdictConfig[verdict] || verdictConfig.unverifiable;

  return (
    <span className={`${config.color} text-white px-3 py-1 rounded-full text-sm font-semibold uppercase`}>
      {config.label}
    </span>
  );
};
