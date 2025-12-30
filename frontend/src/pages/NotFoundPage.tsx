import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/common/Button';

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="max-w-2xl mx-auto px-4 py-16 text-center">
      <h1 className="text-6xl font-bold mb-4">404</h1>
      <p className="text-2xl text-gray-700 mb-8">Page not found</p>
      <Button onClick={() => navigate('/')}>Go Home</Button>
    </div>
  );
};

export default NotFoundPage;
