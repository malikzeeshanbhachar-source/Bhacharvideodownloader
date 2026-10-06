class DownloaderService:
    """Backend placeholder service for future TikTok processing logic."""

    async def inspect(self, url: str) -> dict:
        return {
            "status": "not_ready",
            "message": "Downloader service not implemented yet.",
            "url": url,
            "title": None,
            "author": None,
            "duration": None,
            "formats": [],
        }

    async def download(self, url: str) -> dict:
        return {
            "status": "not_ready",
            "message": "Download service not implemented yet.",
            "url": url,
        }
