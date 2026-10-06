from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.download import router as download_router

app = FastAPI(
    title="BhacharVideoDownloader API",
    version="0.1.0",
    description="Backend foundation for TikTok video downloader. Real download logic comes in Stage 3.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(download_router)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint for the backend service."""
    return {"status": "ok", "service": "bhachar-video-downloader", "version": "0.1.0"}
