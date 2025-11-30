"""
Application configuration using Pydantic BaseSettings (v2).
"""
from functools import lru_cache
from typing import List, Optional, Union

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_name: str = Field("OkeAI", validation_alias="APP_NAME")
    environment: str = Field("development", validation_alias="ENVIRONMENT")
    debug: bool = Field(False, validation_alias="DEBUG")
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")

    allowed_origins: List[str] = Field(default_factory=lambda: ["*"])

    supabase_url: Optional[HttpUrl] = Field(None, validation_alias="SUPABASE_URL")
    supabase_key: Optional[str] = Field(None, validation_alias="SUPABASE_KEY")

    openai_api_key: Optional[str] = Field(None, validation_alias="OPENAI_API_KEY")
    groq_api_key: Optional[str] = Field(None, validation_alias="GROQ_API_KEY")
    gemini_api_key: Optional[str] = Field(None, validation_alias="GEMINI_API_KEY")
    huggingface_api_key: Optional[str] = Field(None, validation_alias="HUGGINGFACE_API_KEY")
    voyage_api_key: Optional[str] = Field(None, validation_alias="VOYAGE_API_KEY")

    embed_model_provider: Optional[str] = Field(None, validation_alias="EMBED_MODEL_PROVIDER")
    llm_provider: Optional[str] = Field(None, validation_alias="LLM_PROVIDER")

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def split_origins(cls, value: Union[str, List[str]]) -> List[str]:
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
