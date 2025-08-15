class VideoGenerationError(Exception):
    """Custom exception for video generation failures"""
    pass

class InvalidAPIKeyError(Exception):
    """Exception for invalid API keys"""
    pass

class FrameGenerationError(Exception):
    """Exception for frame generation failures"""
    pass

class VideoProcessingError(Exception):
    """Exception for video processing failures"""
    pass