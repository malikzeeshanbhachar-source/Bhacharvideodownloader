from typing import Optional

from pydantic import BaseModel, Field


class VideoUrlRequest(BaseModel):
    """Request payload for video URL operations."""

    url: str = Field(..., min_length=1, description="TikTok video URL")


class VideoInfoResponse(BaseModel):
    """Response model for video information endpoint."""

    status: str = Field(
        "scaffold",
        description="Status of the video processing. 'scaffold' means backend foundation is active.",
    )
    message: str = Field(
        description="Human-readable message about the operation state."
    )
    url: Optional[str] = Field(None, description="The URL that was processed.")
    title: Optional[str] = Field(None, description="Video title (if available).")
    author: Optional[str] = Field(None, description="Video author (if available).")
    duration: Optional[str] = Field(None, description="Video duration (if available).")
    formats: list = Field(default_factory=list, description="Available formats (if available).")


class DownloadResponse(BaseModel):
    """Response model for download request endpoint."""

    status: str = Field(
        "scaffold",
        description="Status of the download request. 'scaffold' means backend foundation is active.",
    )
    message: str = Field(
        description="Human-readable message about the download request."
    )
    url: Optional[str] = Field(None, description="The URL that was requested.")
