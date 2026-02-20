@echo off
REM Cloud Run Deployment Script for Windows
REM Usage: deploy.bat YOUR_PROJECT_ID BACKEND_URL

if "%1"=="" (
    echo Usage: deploy.bat YOUR_PROJECT_ID BACKEND_URL
    echo Example: deploy.bat my-project https://portfolio-backend-xxxxx.run.app/api
    exit /b 1
)

set PROJECT_ID=%1
set BACKEND_URL=%2
if "%BACKEND_URL%"=="" (
    set BACKEND_URL=http://localhost:8000/api
)

echo.
echo ========================================
echo Cloud Run Deployment Script
echo ========================================
echo Project ID: %PROJECT_ID%
echo Backend URL: %BACKEND_URL%
echo.

REM Set project
call gcloud config set project %PROJECT_ID%

REM Configure Docker
echo.
echo [1/5] Configuring Docker authentication...
call gcloud auth configure-docker gcr.io

REM Build and push backend
echo.
echo [2/5] Building and pushing backend image...
call docker build -t gcr.io/%PROJECT_ID%/portfolio-backend:latest ./backend
call docker push gcr.io/%PROJECT_ID%/portfolio-backend:latest

REM Build and push frontend
echo.
echo [3/5] Building and pushing frontend image...
call docker build -t gcr.io/%PROJECT_ID%/portfolio-frontend:latest ./frontend
call docker push gcr.io/%PROJECT_ID%/portfolio-frontend:latest

REM Deploy backend
echo.
echo [4/5] Deploying backend to Cloud Run...
for /f "delims=" %%i in ('type .env 2^>nul ^| findstr "MONGO_URL=" ^| cut -d= -f2-') do set MONGO_URL=%%i
for /f "delims=" %%i in ('type .env 2^>nul ^| findstr "EMAIL_USER=" ^| cut -d= -f2-') do set EMAIL_USER=%%i
for /f "delims=" %%i in ('type .env 2^>nul ^| findstr "EMAIL_PASS=" ^| cut -d= -f2-') do set EMAIL_PASS=%%i
for /f "delims=" %%i in ('type .env 2^>nul ^| findstr "EMAIL_TO=" ^| cut -d= -f2-') do set EMAIL_TO=%%i

call gcloud run deploy portfolio-backend ^
  --image gcr.io/%PROJECT_ID%/portfolio-backend:latest ^
  --platform managed ^
  --region us-central1 ^
  --port 8000 ^
  --memory 512Mi ^
  --allow-unauthenticated ^
  --update-env-vars MONGO_URL=%MONGO_URL%,DB_NAME=portfolio_db,EMAIL_USER=%EMAIL_USER%,EMAIL_PASS=%EMAIL_PASS%,EMAIL_TO=%EMAIL_TO%,CORS_ORIGINS=%BACKEND_URL:?api=%

REM Deploy frontend
echo.
echo [5/5] Deploying frontend to Cloud Run...
call gcloud run deploy portfolio-frontend ^
  --image gcr.io/%PROJECT_ID%/portfolio-frontend:latest ^
  --platform managed ^
  --region us-central1 ^
  --port 3000 ^
  --memory 256Mi ^
  --allow-unauthenticated ^
  --update-env-vars REACT_APP_API_URL=%BACKEND_URL%

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
call gcloud run services list
echo.
pause