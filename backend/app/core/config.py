"""Ortam değişkenlerinden okunan uygulama ayarları (12-factor)."""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core import constants


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Uygulama
    PROJECT_NAME: str = "CarePilot"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    # Veritabanı — asyncpg sürücüsü zorunlu (postgresql+asyncpg://...)
    DATABASE_URL: str = "postgresql+asyncpg://carepilot:carepilot@localhost:5432/carepilot"

    # Güvenlik / JWT
    JWT_SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = constants.DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES

    # Yapay Zeka (Gemini) — Sprint 2'de kullanılacak
    GEMINI_API_KEY: str | None = None

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    @field_validator("DATABASE_URL")
    @classmethod
    def _normalize_database_url(cls, value: str) -> str:
        """Railway/Heroku tarzı postgres URL'lerini asyncpg sürücüsüne çevirir.

        Railway, DATABASE_URL'i `postgresql://...` formatında verir; uygulamamız
        ve Alembic async erişim için `postgresql+asyncpg://...` ister.
        """
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+asyncpg://", 1)
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+asyncpg://", 1)
        return value

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Ayarları tek sefer okuyup önbelleğe alır."""
    return Settings()


settings = get_settings()
