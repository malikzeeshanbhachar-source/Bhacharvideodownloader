from pydantic import BaseModel, Field


class VideoUrlRequest(BaseModel):
    url: str = Field(..., min_length=1, description="TikTok video URL to inspect or download")


class VideoInfoResponse(BaseModel):
    status: str = "not_ready"
    message: str = "Backend scaffolding is active. Real video inspection is not implemented yet."
    url: str | None = None
    title: str | None = None
    author: str | None = None
    duration: str | None = None


class DownloadResponse(BaseModel):
    status: str = "not_ready"
    message: str = "Backend scaffolding is active. Real download support is not implemented yet."
    url: str | None = None
