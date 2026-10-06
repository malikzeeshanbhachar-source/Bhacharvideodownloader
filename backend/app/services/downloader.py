from __future__ import annotations

import ipaddress
from typing import Any
from urllib.parse import urlparse

import yt_dlp


class DownloaderService:
    """Real metadata extraction service for Stage 3."""

    @staticmethod
    def validate_url(url: str) -> str:
        """Validate a URL before calling yt-dlp.
        
        Raises ValueError if URL is invalid or points to unsafe targets.
        """
        if url is None:
            raise ValueError("URL is required.")

        cleaned = url.strip()
        if not cleaned:
            raise ValueError("URL is required.")

        parsed = urlparse(cleaned)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("URL is malformed.")

        scheme = parsed.scheme.lower()
        if scheme not in {"http", "https"}:
            raise ValueError("Unsupported URL scheme.")

        hostname = (parsed.hostname or "").lower()
        if not hostname:
            raise ValueError("URL is malformed.")

        # Reject localhost variants
        if hostname in {"localhost", "0.0.0.0", "::1", "[::1]", "localhost.localdomain"}:
            raise ValueError("Localhost URLs are not allowed.")

        # Reject internal/reserved hostnames
        if hostname.endswith(".localhost") or hostname.endswith(".local") or hostname.endswith(".internal"):
            raise ValueError("Internal hostnames are not allowed.")

        # Reject private and reserved IP addresses
        try:
            ip_obj = ipaddress.ip_address(hostname)
        except ValueError:
            ip_obj = None

        if ip_obj is not None and (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_multicast
            or ip_obj.is_reserved
        ):
            raise ValueError("Private or internal network targets are not allowed.")

        return cleaned

    @staticmethod
    def _normalize_format(entry: dict[str, Any]) -> dict[str, Any]:
        """Normalize a single format entry from yt-dlp."""
        width = entry.get("width")
        height = entry.get("height")
        resolution = None
        if width and height:
            resolution = f"{width}x{height}"

        filesize = entry.get("filesize") or entry.get("filesize_approx")
        bitrate = entry.get("tbr")

        has_video = False
        if "vcodec" in entry:
            has_video = entry.get("vcodec") not in (None, "none")

        has_audio = False
        if "acodec" in entry:
            has_audio = entry.get("acodec") not in (None, "none")

        return {
            "format_id": entry.get("format_id"),
            "ext": entry.get("ext"),
            "resolution": resolution,
            "fps": int(entry["fps"]) if entry.get("fps") is not None else None,
            "filesize": int(filesize) if filesize is not None else None,
            "has_video": has_video,
            "has_audio": has_audio,
            "bitrate": int(bitrate) if bitrate is not None else None,
        }

    @staticmethod
    def _normalize_metadata(info: dict[str, Any], original_url: str) -> dict[str, Any]:
        """Normalize yt-dlp extracted metadata to a safe API response format."""
        formats = info.get("formats") or []
        normalized_formats = []
        for entry in formats[:20]:
            if not isinstance(entry, dict):
                continue
            normalized_formats.append(DownloaderService._normalize_format(entry))

        return {
            "id": info.get("id") or info.get("display_id"),
            "title": info.get("title"),
            "uploader": info.get("uploader") or info.get("channel") or info.get("uploader_id"),
            "duration": int(info["duration"]) if info.get("duration") is not None else None,
            "thumbnail": info.get("thumbnail"),
            "webpage_url": info.get("webpage_url") or info.get("original_url") or original_url,
            "extractor": info.get("extractor"),
            "formats": normalized_formats,
        }

    async def inspect(self, url: str) -> dict[str, Any]:
        """Retrieve metadata for a URL without downloading media.
        
        Args:
            url: Public video URL
            
        Returns:
            dict with success=True and normalized video metadata,
            or raises ValueError on validation/extraction failure.
        """
        validated_url = self.validate_url(url)

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "noplaylist": True,
            "extract_flat": False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(validated_url, download=False)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("Unable to retrieve video information.") from exc

        if not isinstance(info, dict):
            raise ValueError("Unable to retrieve video information.")

        return {
            "success": True,
            "video": self._normalize_metadata(info, validated_url),
        }

    async def download(self, url: str) -> dict[str, Any]:
        """Stage 3 intentionally does not implement real downloads.
        
        Returns a not-implemented response.
        """
        return {
            "success": False,
            "error": {
                "code": "DOWNLOAD_NOT_IMPLEMENTED",
                "message": "Actual media downloading is not implemented in Stage 3.",
            },
        }
