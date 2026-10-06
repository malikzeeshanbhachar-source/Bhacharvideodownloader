# BhacharVideoDownloader Backend

## Overview

This is **Stage 2: Backend Foundation** of the BhacharVideoDownloader project.

The backend is a minimal FastAPI application that provides:

- A health-check endpoint
- Route scaffolding for video inspection and downloads
- Service placeholders for future video processing logic
- Basic configuration and request/response models

**No actual video downloading is implemented yet.** That will come in Stage 3.

## Architecture

```
backend/
├── app/
│   ├── __init__.py        # App export
│   ├── main.py            # FastAPI application setup
│   ├── config.py          # Configuration management
│   ├── models.py          # Request/response Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── download.py    # Video inspection and download routes
│   └── services/
│       ├── __init__.py
│       └── downloader.py  # Service layer for future logic
├── tests/
│   ├── __init__.py
│   └── test_health.py     # Health endpoint test
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Dependencies

Only essential packages:

- **fastapi** — Web framework
- **uvicorn** — ASGI server
- **pydantic** — Request/response validation
- **pytest** — Testing framework
- **httpx** — HTTP client for testing

## Setup

### Prerequisites

- Python 3.9 or later

### Installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn app.main:app --reload
```

The server will start on `http://localhost:8000` by default.

### API documentation

Once the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Run tests

```bash
pytest tests/
```

## Endpoints

### Health Check

```
GET /health
```

**Response:**

```json
{
  "status": "ok",
  "service": "bhachar-video-downloader",
  "version": "0.1.0"
}
```

### Video Info (Placeholder)

```
POST /api/videos/info
```

**Request:**

```json
{
  "url": "https://www.tiktok.com/@user/video/1234567890"
}
```

**Response (Stage 2 Scaffold):**

```json
{
  "status": "scaffold",
  "message": "Backend Stage 2 is active. Real video inspection will be implemented in Stage 3.",
  "url": "https://www.tiktok.com/@user/video/1234567890",
  "title": null,
  "author": null,
  "duration": null,
  "formats": []
}
```

### Download Request (Placeholder)

```
POST /api/videos/download
```

**Request:**

```json
{
  "url": "https://www.tiktok.com/@user/video/1234567890"
}
```

**Response (Stage 2 Scaffold):**

```json
{
  "status": "scaffold",
  "message": "Backend Stage 2 is active. Real download handling will be implemented in Stage 3.",
  "url": "https://www.tiktok.com/@user/video/1234567890"
}
```

## Configuration

Set environment variables to customize behavior:

```bash
export DEBUG=true           # Enable debug mode
export HOST=127.0.0.1       # Bind to localhost only
export PORT=9000            # Use port 9000
export ENVIRONMENT=staging  # Set environment label
```

## Deployment Notes

### GitHub Pages Limitation

The repository currently has **no GitHub Pages configured**. This is correct because:

- GitHub Pages only serves static files (HTML, CSS, JavaScript).
- This backend is Python/FastAPI and requires a runtime environment.
- The frontend (HTML/CSS/JS in `frontend/`) can be deployed to GitHub Pages.
- The backend requires a separate hosting service (e.g., Railway, Render, AWS Lambda, or similar).

### Recommended deployment flow (for future stages):

1. **Frontend**: Deploy `frontend/` to GitHub Pages or a static CDN.
2. **Backend**: Deploy `backend/` to a service that supports Python ASGI applications.
3. **Connection**: Configure the frontend's `API_CONFIG.baseUrl` to point to the backend URL.

## No External Dependencies

This backend requires **no external services** to run (no databases, message queues, etc.).
It is intentionally minimal to focus on the core foundation.

## What's Not Included

- ❌ yt-dlp
- ❌ FFmpeg
- ❌ Database (SQL/NoSQL)
- ❌ Message queue (Redis, RabbitMQ, etc.)
- ❌ Authentication/authorization
- ❌ Payment processing
- ❌ Ads or analytics
- ❌ Real video download logic

These will be added in Stage 3 if needed.

## Next Steps

Stage 3 will implement:

1. Real video inspection logic using yt-dlp or similar.
2. Actual download request handling.
3. Real progress tracking and error handling.
4. Integration with the frontend's API configuration.

For now, this backend is ready to accept requests and respond with scaffold messages.
