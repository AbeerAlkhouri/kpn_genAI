import os
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.static_conf import (shared_docs_folder,
    ENV_FILE_PATH,
    APP_NAME,
    APP_VERSION,)


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE_PATH", ENV_FILE_PATH),  # Default to .env,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    APP_NAME: str = APP_NAME
    APP_VERSION: str = APP_VERSION
    SHARED_FOLDER:  pathlib.Path  = shared_docs_folder


    #Azure
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_KEY: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_EMBEDDING_DEPLOYMENT: str
    AZURE_GPT_DEPLOYMENT: str

    # KPN External Data
    KPN_NEWS_URL: str = "https://overons.kpn/en/news"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
