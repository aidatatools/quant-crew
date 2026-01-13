from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    APP_NAME: str = "FastAPI Application"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/dbname"

    TICKERS: str = "2330.TW,TSM,NVDA,GOOG"

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:8080",
        "http://localhost:8000",
    ]

    @property
    def ticker_list(self) -> list[str]:
        """Convert comma-separated tickers string to list."""
        return [ticker.strip() for ticker in self.TICKERS.split(",")]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return v


settings = Settings()
