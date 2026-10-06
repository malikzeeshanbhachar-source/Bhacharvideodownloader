# BhacharVideoDownloader Backend

This directory contains the backend scaffolding for the downloader project.

## Structure

- `app/` contains the FastAPI application, configuration, models, routes, and service placeholders.
- `tests/` contains a minimal health check.

## Notes

- This is a scaffold only.
- No real TikTok download logic is implemented yet.
- No third-party downloader or secret credentials are included.

## Local development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open the API docs at:

- http://localhost:8000/docs
- http://localhost:8000/redoc
