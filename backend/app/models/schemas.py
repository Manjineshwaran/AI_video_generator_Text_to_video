from pydantic import BaseModel, Field

class TextToVideoRequest(BaseModel):
    """Request model for text to video generation"""
    prompt: str = Field(..., example="A beautiful sunset over mountains")
    duration: int = Field(3, gt=1, le=60, description="Duration in seconds (1-60)")
    fps: int = Field(12, gt=1, le=60, description="Frames per second (1-60)")

class VideoResponse(BaseModel):
    """Response model for video generation"""
    message: str
    video_path: str
    download_url: str