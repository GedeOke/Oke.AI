"""
Application configuration using Pydantic BaseSettings.
"""
from functools import lru_cache
from typing import List, Optional

from pydantic import BaseSettings, Field, HttpUrl, validator


class Settings(BaseSettings):
    """
    Centralized application settings loaded from environment variables.
    """

    app_name: str = Field("OkeAI", env="APP_NAME")
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    allowed_origins: List[str] = Field(default_factory=lambda: ["*"])

    supabase_url: Optional[HttpUrl] = Field(None, env="SUPABASE_URL")
    supabase_key: Optional[str] = Field(None, env="SUPABASE_KEY")

    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    groq_api_key: Optional[str] = Field(None, env="GROQ_API_KEY")
    gemini_api_key: Optional[str] = Field(None, env="GEMINI_API_KEY")
    huggingface_api_key: Optional[str] = Field(None, env="HUGGINGFACE_API_KEY")
    voyage_api_key: Optional[str] = Field(None, env="VOYAGE_API_KEY")

    embed_model_provider: Optional[str] = Field(None, env="EMBED_MODEL_PROVIDER")
    llm_provider: Optional[str] = Field(None, env="LLM_PROVIDER")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @validator("allowed_origins", pre=True)
    def split_origins(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return ["*"]


@lru_cache
def get_settings() -> Settings:
    """
    Cached Settings instance to avoid reparsing the environment.
    """
    return Settings()
