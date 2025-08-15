import logging
from pathlib import Path
from datetime import datetime
import os

from app.core.config import settings

def setup_logging():
    """Configure logging for the application"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "simple": {
                "format": "%(levelname)s %(message)s"
            },
        },
        "handlers": {
            "file": {
                "level": settings.LOG_LEVEL,
                "class": "logging.FileHandler",
                "filename": log_file,
                "formatter": "verbose"
            },
            "console": {
                "level": settings.LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "simple"
            },
        },
        "loggers": {
            "": {
                "handlers": ["file", "console"],
                "level": settings.LOG_LEVEL,
                "propagate": True
            },
        }
    }
    
    logging.config.dictConfig(logging_config)