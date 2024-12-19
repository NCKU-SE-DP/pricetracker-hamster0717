from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from functools import lru_cache
import dotenv
import os

dotenv.load_dotenv()
class NewsSettings(BaseSettings):
    OPENAI_APIKEY: str = os.getenv("OPENAI_APIKEY")
    ANTHROPIC_APIKEY: str = os.getenv("ANTHROPIC_APIKEY")
@lru_cache
def get_NewsSettings() -> NewsSettings:
    return NewsSettings()
