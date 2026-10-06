from fastapi import APIRouter, HTTPException

from app.models import DownloadResponse, VideoInfoResponse, VideoUrlRequest

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.post("/info", response_model=VideoInfoResponse)
async def get_video_info(payload: VideoUrlRequest) -> VideoInfoResponse:
    if not payload.url:
        raise HTTPException(status_code=400, detail="URL is required.")

    return VideoInfoResponse(
        status="not_ready",
        message="Backend scaffolding is active. Real video inspection is not implemented yet.",
        url=payload.url,
        title=None,
        author=None,
        duration=None,
    )


@router.post("/download", response_model=DownloadResponse)
async def request_download(payload: VideoUrlRequest) -> DownloadResponse:
    if not payload.url:
        raise HTTPException(status_code=400, detail="URL is required.")

    return DownloadResponse(
        status="not_ready",
        message="Backend scaffolding is active. Real download handling is not implemented yet.",
        url=payload.url,
    )
