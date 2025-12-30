import React from 'react';
import clsx from 'clsx';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, className, onClick }) => {
  return (
    <div className={clsx('card', onClick && 'cursor-pointer', className)} onClick={onClick}>
      {children}
    </div>
  );
};
