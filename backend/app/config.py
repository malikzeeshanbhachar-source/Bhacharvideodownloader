import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings from environment variables or defaults."""

    app_name: str = "BhacharVideoDownloader"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    environment: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()
