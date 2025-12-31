#!/bin/bash

# Shutdown script for Don't Look Up Fact Checker (Linux/Mac)

echo "========================================"
echo "Don't Look Up - Fact Checker Shutdown"
echo "========================================"
echo

echo "Stopping all Docker services..."
echo "- Frontend"
echo "- Backend API"
echo "- Celery Worker"
echo "- Celery Beat"
echo "- PostgreSQL"
echo "- Redis"
echo

docker-compose down

echo
echo "========================================"
echo "Shutdown Complete!"
echo "========================================"
echo
echo "All services have been stopped and containers removed."
echo
echo "Note: Database data is preserved in Docker volumes."
echo "To remove all data, run: docker-compose down -v"
echo
echo "To start again, run: ./startup.sh"
echo
