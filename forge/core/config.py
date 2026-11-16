"""System configuration and environment management for FORGE."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for FORGE platform."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=(),
    )

    # Core settings
    app_name: str = "FORGE Engineering Intelligence Platform"
    version: str = "1.0.0"
    environment: str = Field(default="development", alias="FORGE_ENV")
    debug: bool = Field(default=False, alias="FORGE_DEBUG")

    # Model Provider Settings
    model_provider: Literal["mock", "gemini"] = Field(default="mock", alias="FORGE_MODEL_PROVIDER")
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    gemini_model: str = Field(default="gemini-1.5-flash", alias="FORGE_GEMINI_MODEL")
    temperature: float = Field(default=0.2, alias="FORGE_TEMPERATURE")
    timeout_seconds: int = Field(default=60, alias="FORGE_TIMEOUT_SECONDS")
    max_retries: int = Field(default=3, alias="FORGE_MAX_RETRIES")

    # Orchestration & Revision
    max_revisions: int = Field(default=3, alias="FORGE_MAX_REVISIONS")

    # Storage & Persistence
    database_url: str = Field(default="sqlite:///./forge.db", alias="FORGE_DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="FORGE_REDIS_URL")

    # Observability & Logging
    log_level: str = Field(default="INFO", alias="FORGE_LOG_LEVEL")
    log_format: Literal["json", "text"] = Field(default="text", alias="FORGE_LOG_FORMAT")
    enable_telemetry: bool = Field(default=False, alias="FORGE_ENABLE_TELEMETRY")

    # MLflow Tracking
    mlflow_tracking_uri: str = Field(default="./mlruns", alias="FORGE_MLFLOW_TRACKING_URI")
    mlflow_experiment_name: str = Field(
        default="FORGE_Benchmark_v1.0", alias="FORGE_MLFLOW_EXPERIMENT_NAME"
    )

    def get_masked_api_key(self) -> str:
        """Return masked API key for safe logging."""
        if not self.google_api_key:
            return "[NOT SET]"
        if len(self.google_api_key) <= 8:
            return "********"
        return f"{self.google_api_key[:4]}...{self.google_api_key[-4:]}"


# Global cached settings instance
settings = Settings()
