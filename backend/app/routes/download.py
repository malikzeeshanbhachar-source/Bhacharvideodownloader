from fastapi import APIRouter, HTTPException

from app.models import DownloadResponse, VideoInfoResponse, VideoUrlRequest
from app.services.downloader import DownloaderService

router = APIRouter(prefix="/api/videos", tags=["videos"])
downloader_service = DownloaderService()


@router.post("/info", response_model=VideoInfoResponse)
async def get_video_info(payload: VideoUrlRequest) -> VideoInfoResponse:
    """Inspect video metadata (Stage 2: scaffold only, no real processing yet)."""
    if not payload.url or not payload.url.strip():
        raise HTTPException(status_code=400, detail="URL is required.")

    result = await downloader_service.inspect(payload.url)
    return VideoInfoResponse(**result)


@router.post("/download", response_model=DownloadResponse)
async def request_download(payload: VideoUrlRequest) -> DownloadResponse:
    """Request a download (Stage 2: scaffold only, no real downloading yet)."""
    if not payload.url or not payload.url.strip():
        raise HTTPException(status_code=400, detail="URL is required.")

    result = await downloader_service.download(payload.url)
    return DownloadResponse(**result)
