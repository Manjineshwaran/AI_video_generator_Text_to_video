import os
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Text to Video Generator"
    API_V1_STR: str = "/api/v1"
    VIDEO_OUTPUT_DIR: str = "static/videos"
    FRAME_OUTPUT_DIR: str = "static/frames"
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY")
    ALLOWED_ORIGINS: list = ["*"]
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()


Path(settings.VIDEO_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.FRAME_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)