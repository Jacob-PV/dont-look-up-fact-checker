import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/common/Button';

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-6xl font-bold mb-4 text-primary-900">Don't Look Up</h1>
        <p className="text-2xl text-gray-700 mb-8">
          Automated AI-powered fact-checking with full transparency
        </p>

        <div className="flex gap-4 justify-center">
          <Button onClick={() => navigate('/articles')}>
            View Articles
          </Button>
          <Button variant="secondary" onClick={() => navigate('/about')}>
            Learn More
          </Button>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="card text-center">
          <h3 className="text-xl font-semibold mb-2">Automated Ingestion</h3>
          <p className="text-gray-600">
            Automatically fetches and analyzes articles from trusted news sources
          </p>
        </div>

        <div className="card text-center">
          <h3 className="text-xl font-semibold mb-2">AI-Powered Analysis</h3>
          <p className="text-gray-600">
            Uses LLMs to extract claims and search for evidence
          </p>
        </div>

        <div className="card text-center">
          <h3 className="text-xl font-semibold mb-2">Full Transparency</h3>
          <p className="text-gray-600">
            Shows confidence scores, evidence, and reasoning for all verdicts
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
