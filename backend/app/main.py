from fastapi import FastAPI

from app.routes.download import router as download_router

app = FastAPI(
    title="BhacharVideoDownloader API",
    version="0.1.0",
    description="Backend scaffold for BhacharVideoDownloader. Replace placeholder logic with production implementation as needed.",
)

app.include_router(download_router)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "service": "bhachar-video-downloader"}
