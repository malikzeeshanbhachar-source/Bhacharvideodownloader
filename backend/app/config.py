import os
from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = "BhacharVideoDownloader"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))


settings = Settings()
