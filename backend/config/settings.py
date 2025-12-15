"""Application settings using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = "sqlite:///./addresses.db"

    # Mapbox
    mapbox_access_token: str
    mapbox_base_url: str = "https://api.mapbox.com/search/geocode/v6/forward"

    # Similarity
    default_similarity_method: str = "jaro_winkler"

    # Pagination
    default_page_size: int = 5
    max_page_size: int = 100


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance (singleton pattern)."""
    return Settings()


# Singleton instance
settings = get_settings()