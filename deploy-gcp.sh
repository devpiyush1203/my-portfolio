#!/bin/bash

# Cloud Run Deployment Script
# Usage: ./deploy-gcp.sh YOUR_PROJECT_ID BACKEND_URL

if [ -z "$1" ]; then
    echo "Usage: $0 YOUR_PROJECT_ID [BACKEND_URL]"
    echo "Example: $0 my-project https://portfolio-backend-xxxxx.run.app/api"
    exit 1
fi

PROJECT_ID=$1
BACKEND_URL=${2:-"http://localhost:8000/api"}

echo ""
echo "========================================"
echo "Cloud Run Deployment Script"
echo "========================================"
echo "Project ID: $PROJECT_ID"
echo "Backend URL: $BACKEND_URL"
echo ""

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set project
gcloud config set project $PROJECT_ID

# Configure Docker
echo "[1/5] Configuring Docker authentication..."
gcloud auth configure-docker gcr.io

# Build and push backend
echo ""
echo "[2/5] Building and pushing backend image..."
docker build -t gcr.io/$PROJECT_ID/portfolio-backend:latest ./backend
docker push gcr.io/$PROJECT_ID/portfolio-backend:latest

# Build and push frontend
echo ""
echo "[3/5] Building and pushing frontend image..."
docker build -t gcr.io/$PROJECT_ID/portfolio-frontend:latest ./frontend
docker push gcr.io/$PROJECT_ID/portfolio-frontend:latest

# Deploy backend
echo ""
echo "[4/5] Deploying backend to Cloud Run..."
gcloud run deploy portfolio-backend \
  --image gcr.io/$PROJECT_ID/portfolio-backend:latest \
  --platform managed \
  --region us-central1 \
  --port 8000 \
  --memory 512Mi \
  --allow-unauthenticated \
  --update-env-vars \
    MONGO_URL=$MONGO_URL,\
DB_NAME=portfolio_db,\
EMAIL_USER=$EMAIL_USER,\
EMAIL_PASS=$EMAIL_PASS,\
EMAIL_TO=$EMAIL_TO,\
CORS_ORIGINS=$(echo $BACKEND_URL | sed 's|/api||')

# Deploy frontend
echo ""
echo "[5/5] Deploying frontend to Cloud Run..."
gcloud run deploy portfolio-frontend \
  --image gcr.io/$PROJECT_ID/portfolio-frontend:latest \
  --platform managed \
  --region us-central1 \
  --port 3000 \
  --memory 256Mi \
  --allow-unauthenticated \
  --update-env-vars REACT_APP_API_URL=$BACKEND_URL

echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
gcloud run services list
echo ""