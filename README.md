# Don't Look Up - Automated Fact-Checking Web App

An AI-powered fact-checking application that automatically ingests news articles, extracts verifiable claims, searches for evidence, and presents transparent fact-checks with propaganda detection.

## Features

- **Automated News Ingestion**: Fetches articles from RSS feeds and public news APIs
- **AI-Powered Claim Extraction**: Uses Ollama LLM to identify verifiable factual claims
- **Evidence-Based Fact-Checking**: Searches for supporting and refuting evidence using vector similarity
- **Propaganda Detection**: Identifies manipulation techniques in articles and claims
- **Privacy-First**: Automatic PII detection and redaction before storage
- **Full Transparency**: Shows confidence scores, evidence sources, and reasoning
- **RESTful API**: Programmatic access with rate limiting
- **Modern UI**: Responsive React application with Tailwind CSS

## Tech Stack

### Backend
- **FastAPI** - High-performance async web framework
- **PostgreSQL** - Relational database for structured data
- **Redis** - Caching and message broker
- **Celery** - Background task processing
- **Ollama** - Local LLM inference (server-side only)
- **FAISS** - Vector similarity search
- **spaCy & Presidio** - PII detection and redaction

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** - Utility-first styling
- **React Query** - Server state management
- **React Router** - Client-side routing
- **Recharts** - Data visualization

### DevOps
- **Docker & Docker Compose** - Containerization
- **Alembic** - Database migrations
- **Nginx** - Reverse proxy (production)

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Ollama running locally (for LLM inference)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd dont-look-up-fact-checker
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Ollama** (if not already running)
   ```bash
   # On macOS/Linux
   ollama serve

   # Pull the model
   ollama pull llama2
   ```

4. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - API: http://localhost:8000/api/v1

### Database Initialization

The database will be automatically initialized on first run. To manually run migrations:

```bash
docker-compose exec backend alembic upgrade head
```

### Seed Initial Data

To populate the database with sample news sources:

```bash
docker-compose exec backend python scripts/seed_sources.py
```

## Environment Variables

Key environment variables (see `.env.example` for full list):

```bash
# Database
DATABASE_URL=postgresql://factcheck:password@postgres:5432/factcheck

# Ollama (CRITICAL - Never expose to frontend)
OLLAMA_API_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama2

# Security
SECRET_KEY=your-secret-key-here

# Frontend
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Project Structure

```
dont-look-up-fact-checker/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core utilities (logging, security)
│   │   ├── db/               # Database setup
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   │   ├── llm/          # LLM integration
│   │   │   ├── privacy/      # PII detection & redaction
│   │   │   ├── analysis/     # Claim extraction & fact-checking
│   │   │   └── vector/       # FAISS vector search
│   │   ├── tasks/            # Celery background tasks
│   │   └── main.py           # FastAPI app
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── hooks/            # Custom hooks
│   │   ├── api/              # API client
│   │   └── types/            # TypeScript types
│   ├── package.json
│   └── tailwind.config.js
├── docker/
│   ├── backend/Dockerfile
│   └── frontend/Dockerfile
├── docker-compose.yml
└── README.md
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

### Key Endpoints

- **GET /api/v1/articles** - List articles
- **GET /api/v1/articles/{id}** - Get article details
- **GET /api/v1/claims** - List claims
- **GET /api/v1/claims/{id}** - Get claim with investigation
- **GET /api/v1/investigations** - List investigations
- **GET /api/v1/investigations/{id}** - Get investigation details
- **GET /api/v1/sources** - List news sources
- **GET /api/v1/health** - Health check

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

### Run Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Security & Privacy

- **LLM Security**: All Ollama API calls are server-side only. API URL/key never exposed to frontend.
- **PII Protection**: Automatic detection and redaction of personal information before storage.
- **Rate Limiting**: API rate limits based on tier (free/pro/enterprise).
- **Input Validation**: All inputs validated and sanitized.
- **CORS**: Configured to allow only specified origins.

## Background Tasks

The application uses Celery for background processing:

- **News Ingestion**: Fetches new articles every 30 minutes
- **Claim Extraction**: Processes pending articles every 5 minutes
- **Fact-Checking**: Verifies extracted claims continuously

To run Celery worker (in development):

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

To run Celery beat scheduler:

```bash
celery -A app.tasks.celery_app beat --loglevel=info
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the need for transparent, automated fact-checking
- Built with modern web technologies and AI
- Designed with privacy and transparency as core principles

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with transparency. Powered by AI. Trusted by users.**
