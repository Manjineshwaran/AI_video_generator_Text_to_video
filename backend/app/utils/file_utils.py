import os
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def cleanup_directory(directory: str) -> None:
    """Clean up a directory by removing all its contents"""
    try:
        dir_path = Path(directory)
        if dir_path.exists() and dir_path.is_dir():
            for item in dir_path.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    logger.error(f"Failed to delete {item}: {str(e)}", exc_info=True)
                    
    except Exception as e:
        logger.error(f"Error cleaning up directory {directory}: {str(e)}", exc_info=True)
        raise