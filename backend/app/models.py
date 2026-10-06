from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class VideoUrlRequest(BaseModel):
    """Request payload for video URL operations."""

    url: str = Field(..., min_length=1, description="Video URL to inspect or process")


class FormatInfo(BaseModel):
    """Normalized format metadata returned by yt-dlp."""

    format_id: Optional[str] = Field(None, description="yt-dlp format identifier")
    ext: Optional[str] = Field(None, description="File extension")
    resolution: Optional[str] = Field(None, description="Video resolution, e.g. 1920x1080")
    fps: Optional[int] = Field(None, description="Frame rate for the format")
    filesize: Optional[int] = Field(None, description="File size in bytes")
    has_video: bool = Field(False, description="Whether the format contains video")
    has_audio: bool = Field(False, description="Whether the format contains audio")


class VideoMetadata(BaseModel):
    """Normalized metadata returned for a single video."""

    id: Optional[str] = Field(None, description="Canonical video identifier")
    title: Optional[str] = Field(None, description="Video title")
    uploader: Optional[str] = Field(None, description="Uploader/channel name")
    duration: Optional[int] = Field(None, description="Duration in seconds")
    thumbnail: Optional[str] = Field(None, description="Thumbnail URL")
    webpage_url: Optional[str] = Field(None, description="Original webpage URL")
    extractor: Optional[str] = Field(None, description="Platform extractor name")
    formats: list[FormatInfo] = Field(default_factory=list, description="Safe normalized formats")


class ErrorDetail(BaseModel):
    """Non-sensitive API error payload."""

    code: str = Field(..., description="Stable error code")
    message: str = Field(..., description="Safe human-readable message")


class VideoInfoResponse(BaseModel):
    """Response model for the metadata endpoint."""

    success: bool = Field(True, description="Whether the request succeeded")
    video: Optional[VideoMetadata] = Field(None, description="Video metadata payload")
    error: Optional[ErrorDetail] = Field(None, description="Error payload when the request failed")

    @field_validator("video")
    @classmethod
    def ensure_video_is_present_when_success(cls, value: Optional[VideoMetadata], info: Any) -> Optional[VideoMetadata]:
        if info.data.get("success") is True and value is None:
            raise ValueError("video is required when success is true")
        return value


class DownloadResponse(BaseModel):
    """Placeholder response model for future download workflows."""

    success: bool = Field(False, description="Whether the request succeeded")
    message: Optional[str] = Field(None, description="Human-readable status text")
    error: Optional[ErrorDetail] = Field(None, description="Error payload when the request failed")
