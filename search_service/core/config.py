from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    SEARCH_SERVICE_HOST: str
    SEARCH_SERVICE_PORT: int
    SEARCH_SERVICE_PATH: str
    SEARCH_SERVICE_INDEX_NAME: str

    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..",
            ".env"
        )
    
    @property
    def elastic_search_url(self) -> str:
        return (
            f"http://{self.SEARCH_SERVICE_HOST}:"
            f"{self.SEARCH_SERVICE_PORT}"
            f"{self.SEARCH_SERVICE_PATH}"
        )

@lru_cache()
def get_settings():
    return Settings()