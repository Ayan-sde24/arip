"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the ARIP backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="AI Resume Intelligence Platform")
    app_version: str = Field(default="0.1.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    api_v1_prefix: str = Field(default="/api/v1")

    database_host: str = Field(default="localhost")
    database_port: int = Field(default=5432)
    database_name: str = Field(default="arip")
    database_user: str = Field(default="arip")
    database_password: str = Field(default="arip_password")
    database_url: PostgresDsn = Field(
        default=PostgresDsn(
            "postgresql+psycopg://arip:arip_password@localhost:5432/arip"
        )
    )

    jwt_secret_key: str = Field(default="replace-with-a-secure-random-secret")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=30)

    log_level: str = Field(default="INFO")
    log_file_path: Path = Field(default=Path("logs/arip.log"))
    log_rotation: str = Field(default="10 MB")
    log_retention: str = Field(default="30 days")

    storage_root: Path = Field(default=Path("storage"))
    uploads_root: Path = Field(default=Path("storage/uploads"))
    generated_root: Path = Field(default=Path("storage/generated"))
    resume_upload_dir: Path = Field(default=Path("storage/uploads/resumes"))
    job_upload_dir: Path = Field(default=Path("storage/uploads/jobs"))
    report_output_dir: Path = Field(default=Path("storage/generated/reports"))
    generated_resume_dir: Path = Field(default=Path("storage/generated/resumes"))
    max_upload_size_bytes: int = Field(default=10 * 1024 * 1024)
    allowed_upload_extensions: tuple[str, ...] = Field(default=("pdf", "docx"))
    allowed_upload_mime_types: tuple[str, ...] = Field(
        default=(
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    )

    embedding_model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    openai_api_key: str = Field(default="replace-with-openai-api-key")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()
