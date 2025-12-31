#!/bin/bash

# Startup script for Don't Look Up Fact Checker (Linux/Mac)

echo "========================================"
echo "Don't Look Up - Fact Checker Startup"
echo "========================================"
echo

# Check if .env exists
if [ -f .env ]; then
    echo "[1/5] .env file found"
else
    echo "[1/5] Creating .env from template..."
    cp .env.example .env
    echo ".env created! Edit if needed."
fi
echo

# Start Docker Compose services
echo "[2/5] Starting Docker services..."
echo "- PostgreSQL database"
echo "- Redis"
echo "- Backend API (port 8000)"
echo "- Frontend (port 3000)"
echo "- Celery Worker (RSS ingestion)"
echo "- Celery Beat (scheduler)"
echo
docker-compose up -d --build

# Wait for services to be ready
echo "[3/5] Waiting for services to be ready..."
sleep 10
echo

# Run database migrations
echo "[4/5] Running database migrations..."
docker-compose exec -T backend alembic upgrade head
echo

# Seed RSS sources
echo "[5/5] Seeding RSS news sources..."
docker-compose exec -T backend python scripts/seed_sources.py
echo

echo "========================================"
echo "Startup Complete!"
echo "========================================"
echo
echo "Application is running:"
echo "- Frontend: http://localhost:3000"
echo "- API Docs: http://localhost:8000/docs"
echo "- API: http://localhost:8000/api/v1"
echo
echo "RSS ingestion is active (fetches every 30 minutes)"
echo
echo "To view logs:"
echo "  docker-compose logs -f"
echo "  docker-compose logs -f celery-worker"
echo "  docker-compose logs -f celery-beat"
echo
echo "To shut down, run: ./shutdown.sh"
echo
