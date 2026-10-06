class DownloaderService:
    """Service placeholder for future TikTok video processing.

    Stage 2: Foundation only.
    Stage 3 will add real video inspection and download logic.
    """

    async def inspect(self, url: str) -> dict:
        """Inspect video metadata from a TikTok URL.

        Args:
            url: TikTok video URL

        Returns:
            Dictionary with video metadata.
            Currently returns a scaffold response.
        """
        return {
            "status": "scaffold",
            "message": "Backend Stage 2 is active. Real video inspection will be implemented in Stage 3.",
            "url": url,
            "title": None,
            "author": None,
            "duration": None,
            "formats": [],
        }

    async def download(self, url: str) -> dict:
        """Request a download for a TikTok video.

        Args:
            url: TikTok video URL

        Returns:
            Dictionary with download status.
            Currently returns a scaffold response.
        """
        return {
            "status": "scaffold",
            "message": "Backend Stage 2 is active. Real download handling will be implemented in Stage 3.",
            "url": url,
        }
