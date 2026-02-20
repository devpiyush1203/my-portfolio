# Cloud Run Deployment Guide

This guide walks you through deploying your Portfolio application to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account** - Sign up at [console.cloud.google.com](https://console.cloud.google.com)
2. **Google Cloud SDK** - [Install](https://cloud.google.com/sdk/docs/install)
3. **Docker** - Already installed on your machine
4. **Project ID** - Create a GCP project and note the project ID

## Step 1: Set Up Google Cloud CLI

```bash
# Install Google Cloud SDK
# Windows: Download installer from https://cloud.google.com/sdk/docs/install
# Mac/Linux: curl https://sdk.cloud.google.com | bash

# Authenticate
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## Step 2: Set Up MongoDB Atlas (Database)

Since Cloud Run is serverless and stateless, use MongoDB Atlas (free tier available):

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a cluster
4. Get your connection string: `mongodb+srv://username:password@cluster.mongodb.net/portfolio_db?retryWrites=true&w=majority`
5. Note: Replace `username:password` with your database credentials

## Step 3: Create Environment File

Create `.env.production` in the root directory:

```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/portfolio_db
DB_NAME=portfolio_db
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
EMAIL_TO=recipient-email@gmail.com
CORS_ORIGINS=https://your-frontend-url.run.app
```

**Get Gmail App Password:**
1. Enable 2FA on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate an app password for "Mail" and "Windows"
4. Use that password in `EMAIL_PASS`

## Step 4: Deploy Backend to Cloud Run

```bash
# Navigate to project directory
cd ~/projects/my-portfolio

# Configure Docker authentication
gcloud auth configure-docker gcr.io

# Build and push backend image
docker build -t gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest ./backend
docker push gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest

# Deploy to Cloud Run
gcloud run deploy portfolio-backend \
  --image gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest \
  --platform managed \
  --region us-central1 \
  --port 8000 \
  --memory 512Mi \
  --allow-unauthenticated \
  --set-env-vars MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/portfolio_db,DB_NAME=portfolio_db,EMAIL_USER=your-email@gmail.com,EMAIL_PASS=your-app-password,EMAIL_TO=recipient@gmail.com,CORS_ORIGINS=https://your-frontend-url.run.app
```

**Note:** Replace `YOUR_PROJECT_ID` with your actual GCP project ID.

After deployment, you'll get a URL like: `https://portfolio-backend-xxxxx.run.app`

## Step 5: Update Frontend Environment Variables

Update `frontend/.env` (or create if doesn't exist):

```env
REACT_APP_API_URL=https://portfolio-backend-xxxxx.run.app/api
```

## Step 6: Deploy Frontend to Cloud Run

```bash
# Build and push frontend image
docker build -t gcr.io/YOUR_PROJECT_ID/portfolio-frontend:latest ./frontend
docker push gcr.io/YOUR_PROJECT_ID/portfolio-frontend:latest

# Deploy to Cloud Run
gcloud run deploy portfolio-frontend \
  --image gcr.io/YOUR_PROJECT_ID/portfolio-frontend:latest \
  --platform managed \
  --region us-central1 \
  --port 3000 \
  --memory 256Mi \
  --allow-unauthenticated \
  --set-env-vars REACT_APP_API_URL=https://portfolio-backend-xxxxx.run.app/api
```

After deployment, you'll get a frontend URL like: `https://portfolio-frontend-xxxxx.run.app`

## Step 7: Verify Deployment

```bash
# Check running services
gcloud run services list

# View logs
gcloud run logs read portfolio-backend --limit 50
gcloud run logs read portfolio-frontend --limit 50

# Test the API
curl https://portfolio-backend-xxxxx.run.app/docs
```

## Step 8: Configure Custom Domain (Optional)

Map a custom domain to your Cloud Run services:

```bash
# Add custom domain to backend
gcloud run services update portfolio-backend \
  --region us-central1 \
  --update-env-vars CORS_ORIGINS=https://yourdomain.com

# Add custom domain mapping
gcloud run domain-mappings create \
  --service=portfolio-backend \
  --domain=api.yourdomain.com \
  --region=us-central1

# Repeat for frontend
gcloud run domain-mappings create \
  --service=portfolio-frontend \
  --domain=www.yourdomain.com \
  --region=us-central1
```

Then add DNS records as shown in the console.

## Cleanup (Delete Services)

```bash
gcloud run services delete portfolio-backend --region us-central1
gcloud run services delete portfolio-frontend --region us-central1
```

## Cost Estimates

**Cloud Run Free Tier (per month):**
- 2 million requests
- 360,000 GB-seconds of compute time
- 1 GB of data transfer OUT

**MongoDB Atlas Free Tier:**
- 512 MB storage
- Shared cluster

Your portfolio should easily fit within free tier limits!

## Troubleshooting

### Backend can't connect to MongoDB
- Check MONGO_URL environment variable
- Ensure IP whitelist includes `0.0.0.0/0` in MongoDB Atlas
- Check database credentials

### Frontend can't reach backend
- Verify CORS_ORIGINS in backend matches frontend URL
- Check that backend API URL in frontend `.env` is correct

### 403 Forbidden on API calls
- Update CORS_ORIGINS to include your frontend URL
- Restart backend service after changing env vars

## Summary

Your portfolio is now live on Google Cloud Run with:
- ✅ Auto-scaling backend on Cloud Run
- ✅ Serverless MongoDB on Atlas
- ✅ Static frontend on Cloud Run
- ✅ Free tier eligible
- ✅ Global CDN distribution
- ✅ SSL/TLS encryption by default
