# Quick Start Guide

## Prerequisites

1. **Docker Desktop** installed and running
2. **Ollama** installed and running with llama2 model

### Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
ollama pull llama2

# Windows
# Download from https://ollama.ai/download
# Then run:
ollama serve
ollama pull llama2
```

## Setup (3 Simple Steps)

### Step 1: Setup Environment

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Initialize Database

In a new terminal:

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed news sources
docker-compose exec backend python scripts/seed_sources.py
```

### Step 3: Access Application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API**: http://localhost:8000/api/v1

## That's It!

The application is now running and ready to use.

## What You'll See

1. **Home Page** - Landing page with value proposition
2. **Articles Page** - Will be empty until articles are ingested
3. **About Page** - Explanation of how the system works

## Next Steps

### Add Test Data

To see the application with data:

```bash
# Connect to backend container
docker-compose exec backend python

# In Python shell:
from app.db.session import SessionLocal
from app.models import Article, NewsSource
import uuid

db = SessionLocal()
source = db.query(NewsSource).first()

# Create test article
article = Article(
    source_id=source.id,
    title="Test Article: GDP Growth Reported",
    url="https://example.com/test-article",
    content="The economy grew by 3% in the fourth quarter...",
    status="analyzed"
)
db.add(article)
db.commit()
print(f"Created article: {article.id}")
db.close()
```

Then refresh the Articles page to see your test article!

## Troubleshooting

### Ollama Connection Issues

If you see Ollama connection errors:

1. Make sure Ollama is running: `ollama serve`
2. Check the model is pulled: `ollama list`
3. For Docker on Windows/Mac, the backend uses `host.docker.internal:11434`

### Port Conflicts

If ports are already in use:

1. Stop other services using ports 3000, 8000, 5432, 6379
2. Or edit `docker-compose.yml` to use different ports

### Database Issues

If migrations fail:

```bash
# Restart everything fresh
docker-compose down -v
docker-compose up --build
docker-compose exec backend alembic upgrade head
```

## Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

## Development Mode

The application runs in development mode by default:

- **Backend**: Auto-reloads on file changes
- **Frontend**: Hot module replacement enabled

Just edit files and see changes immediately!

## Need Help?

See the full README.md for comprehensive documentation.
