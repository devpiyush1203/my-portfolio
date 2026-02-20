# Portfolio Docker Setup

This repository contains a full-stack portfolio application with a FastAPI backend and React frontend.

## Prerequisites

- Docker
- Docker Compose

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
EMAIL_TO=recipient-email@gmail.com
```

## Running the Application

1. **Clone the repository and navigate to the project directory**

2. **Build and start the services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Services

- **backend**: FastAPI application (port 8000)
- **frontend**: React application (port 3000)
- **mongo**: MongoDB database (port 27017)

## API Endpoints

- `POST /api/contact/send` - Send contact form message
- `POST /api/resume/upload` - Upload resume file
- `GET /api/resume/download` - Download current resume
- `GET /api/resume/current` - Get resume metadata

## Development

To run in development mode with hot reloading:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

(Note: You'll need to create a separate dev compose file if desired)

## Stopping the Application

```bash
docker-compose down
```

## Volumes

- `mongo_data`: Persists MongoDB data
- `./backend/uploads`: Persists uploaded resume files