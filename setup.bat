@echo off
REM Quick setup script for Windows

echo ========================================
echo Don't Look Up - Fact Checker Setup
echo ========================================
echo.

REM Check if .env exists
if exist .env (
    echo .env file already exists
) else (
    echo Creating .env from template...
    copy .env.example .env
    echo .env created! Please edit if needed.
)

echo.
echo ========================================
echo Starting Docker Compose...
echo ========================================
echo.
echo This will start:
echo - PostgreSQL database
echo - Redis
echo - Backend API (port 8000)
echo - Frontend (port 3000)
echo.

docker-compose up --build

echo.
echo Setup complete!
echo.
echo Access the application at:
echo - Frontend: http://localhost:3000
echo - API Docs: http://localhost:8000/docs
echo - API: http://localhost:8000/api/v1
