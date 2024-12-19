from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from functools import lru_cache
import dotenv
import os

dotenv.load_dotenv()
class NewsSettings(BaseSettings):
    OPENAI_APIKEY: str
    ANTHROPIC_APIKEY: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
@lru_cache
def get_NewsSettings() -> NewsSettings:
    return NewsSettings()
