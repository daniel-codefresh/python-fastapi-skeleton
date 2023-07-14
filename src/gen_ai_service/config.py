from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    api_v1_prefix: str = "/api/v1"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
