# Cloud Run: Troubleshooting Guide

## Common Issues & Solutions

### 1. "Timeout waiting for service to be ready"

**Cause:** Application takes too long to start

**Solution:**
```bash
# Increase timeout and memory
gcloud run deploy portfolio-backend \
  --image gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest \
  --memory 512Mi \
  --timeout 300
```

---

### 2. "Backend image not found"

**Error:** `image not found: gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest`

**Solution:**
```bash
# Verify image was pushed
gcloud container images list

# Rebuild and push again
docker build -t gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest ./backend
docker push gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest
```

---

### 3. "Frontend can't connect to backend"

**Error:** 404 or CORS errors in frontend

**Solution:**
- Check backend CORS environment variable:
  ```bash
  gcloud run services describe portfolio-backend --region us-central1
  ```
- Update CORS to match frontend URL:
  ```bash
  gcloud run services update portfolio-backend \
    --update-env-vars CORS_ORIGINS=https://portfolio-frontend-xxxxx.run.app
  ```

---

### 4. "MongoDB connection failed"

**Error:** `MongoNetworkError: Failed to connect`

**Solutions:**

a) Check connection string:
```bash
gcloud run services describe portfolio-backend --region us-central1 | grep MONGO_URL
```

b) Verify MongoDB Atlas whitelist includes `0.0.0.0/0`:
- Go to [cloud.mongodb.com](https://cloud.mongodb.com)
- Security > Network Access
- Add IP `0.0.0.0/0`

c) Test connection locally:
```bash
python -c "from pymongo import MongoClient; MongoClient('YOUR_MONGO_URL').server_info()"
```

---

### 5. "Out of memory" errors

**Error:** `Container terminated with exit code 137`

**Solution:**
```bash
# Increase memory
gcloud run services update portfolio-backend \
  --memory 1Gi --region us-central1

gcloud run services update portfolio-frontend \
  --memory 512Mi --region us-central1
```

---

### 6. "Email not sending"

**Error:** SMTPAuthenticationError

**Solutions:**

a) Verify Gmail app password (not regular password):
- [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- Regenerate app password
- Update in Cloud Run

```bash
gcloud run services update portfolio-backend \
  --update-env-vars EMAIL_PASS=your-new-app-password \
  --region us-central1
```

b) Enable Less Secure Apps (alternative):
- [myaccount.google.com/security](https://myaccount.google.com/security)
- Turn on "Less secure app access"

---

### 7. "Permission denied" on gcloud commands

**Error:** `ERROR: (gcloud.run.deploy) User does not have permission`

**Solution:**
```bash
# Give yourself permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member=user:YOUR_EMAIL@gmail.com \
  --role=roles/run.admin

# Enable billing
# Go to console.cloud.google.com > Billing
```

---

### 8. "Cannot push to container registry"

**Error:** `denied: Token exchange failed`

**Solution:**
```bash
# Re-authenticate Docker
gcloud auth configure-docker gcr.io

# Verify credentials
gcloud auth list
```

---

### 9. "Port not listening"

**Error:** `Cloud Run error: The user-provided container failed to start and listen on the port defined provided by the PORT environment variable`

**Solutions:**

a) Verify Dockerfile exposes correct port:
```dockerfile
EXPOSE 8000  # Backend
EXPOSE 3000  # Frontend
```

b) Verify app listens on `0.0.0.0` (not `localhost`):
```python
# In server.py
uvicorn.run(app, host="0.0.0.0", port=8000)
```

c) Set PORT env variable:
```bash
gcloud run deploy portfolio-backend \
  --port 8000 \
  --region us-central1
```

---

### 10. View Logs

```bash
# Last 50 logs
gcloud run logs read portfolio-backend --limit 50

# Follow logs in real-time
gcloud run logs read portfolio-backend --limit 100 --follow

# View in Cloud Console
# https://console.cloud.google.com/logs
```

---

### 11. Rollback to Previous Version

```bash
# List revisions
gcloud run revisions list --service=portfolio-backend --region=us-central1

# Set traffic to previous revision
gcloud run services update-traffic portfolio-backend \
  --to-revisions REVISION_NAME=100 \
  --region us-central1
```

---

### 12. Delete a Service

```bash
gcloud run services delete portfolio-backend --region us-central1
gcloud run services delete portfolio-frontend --region us-central1
```

---

## Performance Optimization

### Reduce Cold Start Time

```bash
# Keep service warm with scheduler
gcloud scheduler jobs create app-engine keep-backend-warm \
  --schedule="*/5 * * * *" \
  --http-method=GET \
  --uri=https://portfolio-backend-xxxxx.run.app/
```

### Use Cloud CDN

```bash
gcloud run services update portfolio-frontend \
  --ingress internal \
  --region us-central1
```

### Monitor Performance

```bash
# View metrics
gcloud run services describe portfolio-backend --region us-central1

# Open console
gcloud console run
```

---

## Quick Commands Reference

```bash
# Describe service
gcloud run services describe portfolio-backend --region us-central1

# Update environment variable
gcloud run services update portfolio-backend \
  --update-env-vars KEY=VALUE \
  --region us-central1

# View all services
gcloud run services list

# Delete service
gcloud run services delete portfolio-backend --region us-central1

# View logs
gcloud run logs read portfolio-backend --limit 50

# Redeploy service
gcloud run deploy portfolio-backend \
  --image gcr.io/YOUR_PROJECT_ID/portfolio-backend:latest \
  --region us-central1
```

---

## Need More Help?

- [Cloud Run Docs](https://cloud.google.com/run/docs)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Cloud Run Samples](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/run)
