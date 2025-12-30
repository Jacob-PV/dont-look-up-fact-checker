import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Header: React.FC = () => {
  const navigate = useNavigate();

  return (
    <header className="bg-primary-900 text-white sticky top-0 z-50 shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="text-2xl font-bold font-heading">
            Don't Look Up
          </Link>

          <nav className="flex gap-6">
            <Link to="/" className="hover:text-primary-300 transition">
              Home
            </Link>
            <Link to="/articles" className="hover:text-primary-300 transition">
              Articles
            </Link>
            <Link to="/investigations" className="hover:text-primary-300 transition">
              Investigations
            </Link>
            <Link to="/dashboard" className="hover:text-primary-300 transition">
              Dashboard
            </Link>
            <Link to="/about" className="hover:text-primary-300 transition">
              About
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
