from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.models import DownloadResponse, ErrorDetail, VideoInfoResponse, VideoUrlRequest
from app.services.downloader import DownloaderService

router = APIRouter(prefix="/api/videos", tags=["videos"])
downloader_service = DownloaderService()


async def _inspect_url(url: str) -> VideoInfoResponse | JSONResponse:
    """Internal helper to validate URL and extract metadata."""
    try:
        result = await downloader_service.inspect(url)
        return VideoInfoResponse(**result)
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": {"code": "INVALID_URL", "message": str(exc)},
            },
        )
    except Exception:  # noqa: BLE001
        return JSONResponse(
            status_code=502,
            content={
                "success": False,
                "error": {
                    "code": "VIDEO_INFO_FAILED",
                    "message": "Unable to retrieve video information.",
                },
            },
        )


@router.get("/info")
async def get_video_info_query(url: str | None = Query(default=None, description="Video URL to inspect")) -> VideoInfoResponse | JSONResponse:
    """Retrieve metadata for a public video URL using GET query parameter."""
    if url is None or not url.strip():
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": {"code": "INVALID_URL", "message": "URL is required."},
            },
        )
    return await _inspect_url(url)


@router.post("/info", response_model=VideoInfoResponse)
async def get_video_info_post(payload: VideoUrlRequest) -> VideoInfoResponse | JSONResponse:
    """Retrieve metadata for a public video URL using POST body."""
    if not payload.url or not payload.url.strip():
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": {"code": "INVALID_URL", "message": "URL is required."},
            },
        )
    return await _inspect_url(payload.url)


@router.post("/download", response_model=DownloadResponse)
async def request_download(payload: VideoUrlRequest) -> DownloadResponse:
    """Stage 3 intentionally does not implement actual downloads."""
    if not payload.url or not payload.url.strip():
        return DownloadResponse(
            success=False,
            error=ErrorDetail(code="INVALID_URL", message="URL is required."),
        )

    result = await downloader_service.download(payload.url)
    return DownloadResponse(**result)
