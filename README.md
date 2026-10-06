# Changelog

## [Stage 3]
- Added real yt-dlp metadata extraction using the Python API
- Added backend URL validation for empty, malformed, unsupported, and local/internal URLs
- Added normalized metadata and format models with safe output schema
- Added `GET /api/videos/info?url=<URL>` and retained POST compatibility
- Added structured error responses without exposing tracebacks
- Added tests for validation and mocked metadata extraction
- Updated the frontend to consume the real metadata endpoint shape
- Updated project documentation to reflect the verified Stage 3 state
