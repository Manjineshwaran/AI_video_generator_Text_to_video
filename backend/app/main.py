import os
import uvicorn
from fastapi import FastAPI, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import logging
from typing import Optional

from app.core.config import settings
from app.core.logger import setup_logging
from app.models.schemas import TextToVideoRequest, VideoResponse
from app.services.video_service import generate_video_from_text

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Text to Video Generator API",
    description="API for generating videos from text prompts using Stable Diffusion",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (videos) directly for reliable streaming
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Text to Video Generator API"}

@app.post("/generate-video", response_model=VideoResponse)
async def text_to_video(request: TextToVideoRequest):
    """
    Generate video from text prompt
    
    Args:
        prompt: Text prompt for video generation
        duration: Duration of video in seconds (default 3)
        fps: Frames per second (default 12)
    
    Returns:
        Video file path and metadata
    """
    try:
        logger.info(f"Received request to generate video for prompt: {request.prompt}")
        
        video_path = generate_video_from_text(
            prompt=request.prompt,
            duration=request.duration,
            fps=request.fps
        )
        
        if not video_path or not Path(video_path).exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Video generation failed"
            )
        
        # Return just the filename for easier frontend handling
        video_filename = Path(video_path).name
        return {
            "message": "Video generated successfully",
            "video_path": video_filename,
            "download_url": f"/download-video?path={video_filename}"
        }
        
    except Exception as e:
        logger.error(f"Error generating video: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating video: {str(e)}"
        )

@app.options("/download-video")
async def download_video_options():
    """Handle CORS preflight requests for video download"""
    return {"message": "OK"}

@app.get("/download-video")
async def download_video(path: str, download: bool = False):
    """
    Download generated video file
    
    Args:
        path: Path to the video file
    
    Returns:
        Video file as attachment
    """
    try:
        logger.info(f"Download request - path: {path}, download: {download}")
        # Normalize requested path. Accept either:
        # - absolute paths
        # - paths already starting with settings.VIDEO_OUTPUT_DIR
        # - bare filenames (we will join to VIDEO_OUTPUT_DIR)
        base_dir = Path(settings.VIDEO_OUTPUT_DIR).resolve()
        # Always serve by filename to avoid cwd/relative path confusion
        filename = Path(path).name
        requested_path = (base_dir / filename).resolve()
        
        logger.info(f"Base dir: {base_dir}")
        logger.info(f"Requested filename: {filename}")
        logger.info(f"Requested path: {requested_path}")
        logger.info(f"File exists: {requested_path.exists()}")

        # Security: ensure requested file is inside base_dir and exists
        if not requested_path.exists() or base_dir not in requested_path.parents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video file not found"
            )
            
        # Serve inline by default so the browser <video> tag can play it
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Accept-Ranges": "bytes",
            "Content-Type": "video/mp4",
        }
        
        if download:
            return FileResponse(
                str(requested_path),
                media_type="video/mp4",
                filename=requested_path.name,
                headers=headers
            )
        else:
            return FileResponse(
                str(requested_path),
                media_type="video/mp4",
                headers=headers
            )
        
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading video: {str(e)}"
        )

@app.get("/list-videos")
async def list_videos():
    """
    List all generated videos
    
    Returns:
        List of available videos
    """
    try:
        video_dir = Path(settings.VIDEO_OUTPUT_DIR)
        videos = [f.name for f in video_dir.glob("*.mp4") if f.is_file()]
        logger.info(f"Found {len(videos)} videos: {videos}")
        return {"videos": videos}
        
    except Exception as e:
        logger.error(f"Error listing videos: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing videos: {str(e)}"
        )

@app.get("/test-video/{filename}")
async def test_video(filename: str):
    """
    Test endpoint to verify video file access and serve video
    """
    try:
        base_dir = Path(settings.VIDEO_OUTPUT_DIR).resolve()
        requested_path = (base_dir / filename).resolve()
        
        logger.info(f"Test video - filename: {filename}")
        logger.info(f"Test video - base_dir: {base_dir}")
        logger.info(f"Test video - requested_path: {requested_path}")
        logger.info(f"Test video - exists: {requested_path.exists()}")
        
        if not requested_path.exists():
            return {"error": "File not found", "path": str(requested_path)}
        
        # Serve the video file with proper headers
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Accept-Ranges": "bytes",
            "Content-Type": "video/mp4",
            "Content-Length": str(requested_path.stat().st_size),
        }
        
        return FileResponse(
            str(requested_path),
            media_type="video/mp4",
            headers=headers
        )
        
    except Exception as e:
        logger.error(f"Error testing video: {str(e)}", exc_info=True)
        return {"error": str(e)}

@app.get("/stream-video/{filename}")
async def stream_video(filename: str):
    """
    Stream video file with proper CORS headers for browser playback
    """
    try:
        base_dir = Path(settings.VIDEO_OUTPUT_DIR).resolve()
        requested_path = (base_dir / filename).resolve()
        
        logger.info(f"Stream video - filename: {filename}")
        logger.info(f"Stream video - requested_path: {requested_path}")
        logger.info(f"Stream video - exists: {requested_path.exists()}")
        
        if not requested_path.exists() or base_dir not in requested_path.parents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video file not found"
            )
        
        # Headers optimized for video streaming
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Accept-Ranges": "bytes",
            "Content-Type": "video/mp4",
            "Content-Length": str(requested_path.stat().st_size),
        }
        
        return FileResponse(
            str(requested_path),
            media_type="video/mp4",
            headers=headers
        )
        
    except Exception as e:
        logger.error(f"Error streaming video: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error streaming video: {str(e)}"
        )
    
