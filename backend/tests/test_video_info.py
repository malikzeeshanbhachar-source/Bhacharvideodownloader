from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """Health endpoint regression test."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "bhachar-video-downloader"


def test_missing_url_query_parameter() -> None:
    """Missing URL query parameter should be rejected."""
    response = client.get("/api/videos/info")
    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "INVALID_URL"
    assert "required" in payload["error"]["message"].lower()


def test_empty_url_rejected() -> None:
    """Empty URL should be rejected."""
    response = client.get("/api/videos/info", params={"url": ""})
    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "INVALID_URL"


def test_malformed_url_rejected() -> None:
    """Malformed URL should be rejected."""
    response = client.get("/api/videos/info", params={"url": "not-a-url"})
    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "INVALID_URL"


def test_unsupported_scheme_rejected() -> None:
    """URL with unsupported scheme (ftp://) should be rejected."""
    response = client.get("/api/videos/info", params={"url": "ftp://example.com/video"})
    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "INVALID_URL"
    assert "scheme" in payload["error"]["message"].lower()


def test_localhost_url_rejected() -> None:
    """Localhost URL should be rejected (SSRF protection)."""
    response = client.get("/api/videos/info", params={"url": "http://localhost:8000/video"})
    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False


def test_loopback_ip_rejected() -> None:
    """Loopback IP (127.0.0.1) should be rejected (SSRF protection)."""
    response = client.get("/api/videos/info", params={"url": "http://127.0.0.1:8000/video"})
    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False


def test_private_ip_rejected() -> None:
    """Private IP (192.168.x.x) should be rejected (SSRF protection)."""
    response = client.get("/api/videos/info", params={"url": "http://192.168.1.1/video"})
    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False


def test_internal_hostname_rejected() -> None:
    """Internal hostname should be rejected (SSRF protection)."""
    response = client.get("/api/videos/info", params={"url": "http://internalserver.local/video"})
    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False


def test_metadata_models_validation() -> None:
    """Test that metadata models validate correctly."""
    from app.models import FormatInfo, VideoMetadata

    format_info = FormatInfo(
        format_id="18",
        ext="mp4",
        resolution="640x360",
        fps=30,
        filesize=123456,
        has_video=True,
        has_audio=True,
        bitrate=500,
    )

    metadata = VideoMetadata(
        id="abc123",
        title="Test video",
        uploader="Test uploader",
        duration=123,
        thumbnail="https://example.com/thumb.jpg",
        webpage_url="https://example.com/video",
        extractor="generic",
        formats=[format_info],
    )

    assert metadata.id == "abc123"
    assert metadata.title == "Test video"
    assert metadata.formats[0].resolution == "640x360"
    assert metadata.formats[0].has_video is True


@patch("app.services.downloader.yt_dlp.YoutubeDL.extract_info")
def test_successful_metadata_extraction(mock_extract: Any) -> None:
    """Test successful metadata extraction with mocked yt-dlp."""
    mock_extract.return_value = {
        "id": "video123",
        "title": "Test video",
        "uploader": "Test channel",
        "duration": 120,
        "thumbnail": "https://example.com/thumb.jpg",
        "webpage_url": "https://example.com/video",
        "extractor": "generic",
        "formats": [
            {
                "format_id": "18",
                "ext": "mp4",
                "width": 640,
                "height": 360,
                "fps": 30,
                "filesize": 123456,
                "vcodec": "avc1",
                "acodec": "mp4a",
                "tbr": 500,
            }
        ],
    }

    response = client.get(
        "/api/videos/info",
        params={"url": "https://www.youtube.com/watch?v=video123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["video"]["id"] == "video123"
    assert payload["video"]["title"] == "Test video"
    assert payload["video"]["formats"][0]["resolution"] == "640x360"
    assert payload["video"]["formats"][0]["has_video"] is True
    assert payload["video"]["formats"][0]["has_audio"] is True


@patch("app.services.downloader.yt_dlp.YoutubeDL.extract_info")
def test_yt_dlp_failure_returns_safe_error(mock_extract: Any) -> None:
    """Test that yt-dlp failures return safe structured errors."""
    mock_extract.side_effect = Exception("Network error from yt-dlp")

    response = client.get(
        "/api/videos/info",
        params={"url": "https://www.youtube.com/watch?v=video123"},
    )

    assert response.status_code == 502
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "VIDEO_INFO_FAILED"
    assert "Unable to retrieve" in payload["error"]["message"]


def test_post_video_info_still_works() -> None:
    """Test that POST /api/videos/info still works (backward compatibility)."""
    with patch("app.services.downloader.yt_dlp.YoutubeDL.extract_info") as mock_extract:
        mock_extract.return_value = {
            "id": "xyz789",
            "title": "POST test video",
            "uploader": "POST test uploader",
            "duration": 90,
            "thumbnail": "https://example.com/thumb2.jpg",
            "webpage_url": "https://example.com/video2",
            "extractor": "generic",
            "formats": [],
        }

        response = client.post("/api/videos/info", json={"url": "https://example.com/video2"})
        assert response.status_code == 200
        payload = response.json()
        assert payload["success"] is True
        assert payload["video"]["id"] == "xyz789"
        assert payload["video"]["title"] == "POST test video"


def test_download_endpoint_not_implemented() -> None:
    """Test that download endpoint returns not-implemented response."""
    response = client.post("/api/videos/download", json={"url": "https://example.com/video"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "DOWNLOAD_NOT_IMPLEMENTED"


def test_format_normalization_with_all_fields() -> None:
    """Test that format normalization includes all expected fields."""
    with patch("app.services.downloader.yt_dlp.YoutubeDL.extract_info") as mock_extract:
        mock_extract.return_value = {
            "id": "test123",
            "title": "Format test",
            "uploader": "Test",
            "duration": 60,
            "thumbnail": None,
            "webpage_url": "https://example.com/test",
            "extractor": "test",
            "formats": [
                {
                    "format_id": "1",
                    "ext": "mp4",
                    "width": 1920,
                    "height": 1080,
                    "fps": 60,
                    "filesize": 1000000,
                    "vcodec": "vp9",
                    "acodec": "opus",
                    "tbr": 1500,
                }
            ],
        }

        response = client.get("/api/videos/info", params={"url": "https://example.com/test"})
        assert response.status_code == 200
        payload = response.json()
        fmt = payload["video"]["formats"][0]
        assert fmt["format_id"] == "1"
        assert fmt["ext"] == "mp4"
        assert fmt["resolution"] == "1920x1080"
        assert fmt["fps"] == 60
        assert fmt["filesize"] == 1000000
        assert fmt["has_video"] is True
        assert fmt["has_audio"] is True
        assert fmt["bitrate"] == 1500
