from pathlib import Path
from typing import Any

import yaml
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "app" / "config"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Application settings
    APP_NAME: str = "Quant-Crew AI Investment Research"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/dbname"

    # Stock tickers (fallback if YAML not used)
    TICKERS: str = "2330.TW,TSM,NVDA,GOOG"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Frontend
        "http://localhost:8080",
        "http://localhost:8000",
    ]

    # AI/LLM settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 4000

    # LangSmith (optional)
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "quant-research-warroom"

    # Report settings
    REPORT_OUTPUT_DIR: str = "outputs/weekly_reports"
    CHART_OUTPUT_DIR: str = "outputs/charts"

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


class ConfigLoader:
    """Utility class to load YAML configuration files."""

    def __init__(self, config_dir: Path = CONFIG_DIR):
        self.config_dir = config_dir
        self._agent_config = None
        self._stock_watchlist = None

    def load_yaml(self, filename: str) -> dict[str, Any]:
        """Load a YAML configuration file."""
        file_path = self.config_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @property
    def agent_config(self) -> dict[str, Any]:
        """Load agent configuration from YAML."""
        if self._agent_config is None:
            self._agent_config = self.load_yaml("agent_config.yaml")
        return self._agent_config

    @property
    def stock_watchlist(self) -> dict[str, Any]:
        """Load stock watchlist from YAML."""
        if self._stock_watchlist is None:
            self._stock_watchlist = self.load_yaml("stock_watchlist.yaml")
        return self._stock_watchlist

    def get_watchlist_symbols(self) -> list[str]:
        """Get all stock symbols from watchlist."""
        watchlist = self.stock_watchlist
        symbols = []

        for region in ["taiwan", "us"]:
            if region in watchlist.get("stocks", {}):
                symbols.extend([stock["symbol"] for stock in watchlist["stocks"][region]])

        return symbols

    def get_agent_settings(self, agent_name: str) -> dict[str, Any]:
        """Get configuration for a specific agent."""
        config = self.agent_config
        return config.get("agents", {}).get(agent_name, {})

    def get_llm_settings(self) -> dict[str, Any]:
        """Get LLM configuration."""
        config = self.agent_config
        return config.get("llm", {})


# Global instances
settings = Settings()
config_loader = ConfigLoader()
