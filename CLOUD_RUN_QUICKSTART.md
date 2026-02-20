# Cloud Run: Quick Start (5 Minutes)

## 1. Prerequisites
```bash
# Install Google Cloud SDK
# Windows: https://cloud.google.com/sdk/docs/install
# Mac: brew install google-cloud-sdk
# Linux: https://cloud.google.com/sdk/docs/install

gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

## 2. Set Up Database (MongoDB Atlas)

- Sign up: [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Create free cluster
- Get connection string: `mongodb+srv://user:pass@cluster.mongodb.net/portfolio_db`
- Add whitelist IP: `0.0.0.0/0` (for Cloud Run)

## 3. Prepare Environment Variables

Edit `.env` in the project root:
```env
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/portfolio_db
DB_NAME=portfolio_db
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-gmail-app-password
EMAIL_TO=recipient@gmail.com
```

## 4. Deploy with One Command

**On Linux/Mac:**
```bash
chmod +x deploy-gcp.sh
./deploy-gcp.sh YOUR_PROJECT_ID
```

**On Windows:**
```cmd
deploy-gcp.bat YOUR_PROJECT_ID
```

## 5. Access Your App

```bash
gcloud run services list
```

You'll see URLs like:
- Frontend: `https://portfolio-frontend-xxxxx.run.app`
- Backend: `https://portfolio-backend-xxxxx.run.app`

## Verify It Works

```bash
# Check backend is running
curl https://portfolio-backend-xxxxx.run.app/docs

# Check frontend
open https://portfolio-frontend-xxxxx.run.app
```

## Cost

- **Free tier covers:** 2M requests/mo, 360,000 GB-seconds/mo
- Your portfolio = ~$0/month on Cloud Run
- MongoDB Atlas free: 512MB storage

## Next Steps

- [Add custom domain](https://cloud.google.com/run/docs/mapping-custom-domains)
- [Set up CI/CD with GitHub](https://cloud.google.com/run/docs/quickstarts/build-and-deploy)
- [Monitor performance](https://console.cloud.google.com/run)

Done! Your portfolio is now live! 🚀
