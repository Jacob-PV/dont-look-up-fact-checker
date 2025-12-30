import React from 'react';

const AboutPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6">About Don't Look Up</h1>

      <div className="prose max-w-none">
        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Our Mission</h2>
          <p className="text-gray-700 mb-4">
            Don't Look Up is an automated fact-checking platform that uses AI to verify claims
            in news articles with full transparency. Our goal is to help people navigate the
            information landscape with confidence.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">How It Works</h2>
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li>We automatically ingest articles from trusted news sources</li>
            <li>AI extracts verifiable factual claims from each article</li>
            <li>Our system searches for supporting and refuting evidence</li>
            <li>Claims are analyzed and assigned a verdict with confidence score</li>
            <li>All evidence and reasoning is shown transparently to users</li>
          </ol>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Privacy & Transparency</h2>
          <p className="text-gray-700 mb-4">
            We take privacy seriously. All personal information is automatically detected
            and redacted before storage. Our fact-checking process is fully transparent -
            we show you the evidence, sources, and reasoning behind every verdict.
          </p>
        </section>
      </div>
    </div>
  );
};

export default AboutPage;
