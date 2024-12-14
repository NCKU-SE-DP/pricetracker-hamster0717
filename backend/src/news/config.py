from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from functools import lru_cache
class NewsSettings(BaseSettings):
    Openai_APIKEY: str = Field(..., description="OpenAI API key")
    Anthropic_APIKEY: str = Field(..., description="Anthropic API key")

    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        env_file_encoding = "utf-8"
        env_prefix = "AI_"
@lru_cache
def get_NewsSettings() -> NewsSettings:
    return NewsSettings()
