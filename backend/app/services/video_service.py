import os
import time
import logging
from pathlib import Path
import shutil
import requests
from PIL import Image
import cv2

from app.core.config import settings
from app.core.exceptions import (
    VideoGenerationError,
    InvalidAPIKeyError,
    FrameGenerationError,
    VideoProcessingError
)
from app.utils.file_utils import cleanup_directory
from app.utils.video_utils import generate_transitions, create_video_from_frames

logger = logging.getLogger(__name__)

def generate_frames_from_text(prompt: str, num_images: int = 5) -> list:
    """Generate images from text using Stable Diffusion API"""
    try:
        api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        api_key = settings.HUGGINGFACE_API_KEY
        print(f"Loaded HuggingFace API key: {api_key}")
        if not api_key:
            raise InvalidAPIKeyError("HuggingFace API key not configured")
        
        headers = {"Authorization": f"Bearer {api_key}"}
        generated_images = []
        
        Path(settings.FRAME_OUTPUT_DIR).mkdir(exist_ok=True)
        
        for i in range(num_images):
            try:
                response = requests.post(
                    api_url,
                    headers=headers,
                    json={"inputs": prompt, "options": {"wait_for_model": True}}
                )
                
                if response.status_code == 200:
                    img_path = str(Path(settings.FRAME_OUTPUT_DIR) / f"frame_{i:03d}.png")
                    with open(img_path, 'wb') as f:
                        f.write(response.content)
                    generated_images.append(img_path)
                    logger.info(f"Generated frame {i+1}/{num_images}")
                else:
                    error_msg = f"API Error {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    raise FrameGenerationError(error_msg)
                
                time.sleep(3)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Failed to generate frame {i+1}: {str(e)}", exc_info=True)
                continue
        
        if not generated_images:
            raise FrameGenerationError("No frames were generated successfully")
            
        return generated_images
        
    except Exception as e:
        logger.error(f"Error in frame generation: {str(e)}", exc_info=True)
        raise FrameGenerationError(f"Frame generation failed: {str(e)}")

def generate_video_from_text(prompt: str, duration: int = 3, fps: int = 12) -> str:
    """Main function to convert text to video"""
    try:
        logger.info(f"Starting video generation for prompt: '{prompt}'")
        
        # Calculate required frames
        total_frames = duration * fps
        key_frames = max(3, total_frames // 10)
        logger.info(f"Generating {key_frames} key frames for {total_frames} total frames")
        
        # Step 1: Generate key images
        images = generate_frames_from_text(prompt, num_images=key_frames)
        
        # Step 2: Create transitions
        logger.info("Creating transitions between frames")
        all_frames = generate_transitions(images, output_dir=settings.FRAME_OUTPUT_DIR)
        
        # Adjust frame count if needed
        if len(all_frames) > total_frames:
            all_frames = all_frames[:total_frames]
        
        # Step 3: Make video
        logger.info(f"Compiling {len(all_frames)} frames into video")
        video_filename = f"video_{int(time.time())}.mp4"
        video_path = str(Path(settings.VIDEO_OUTPUT_DIR) / video_filename)
        
        create_video_from_frames(all_frames, output_file=video_path, fps=fps)
        
        # Cleanup frames directory
        cleanup_directory(settings.FRAME_OUTPUT_DIR)
        
        logger.info(f"Video successfully created at {video_path}")
        return video_path
        
    except Exception as e:
        logger.error(f"Video generation failed: {str(e)}", exc_info=True)
        # Cleanup in case of failure
        cleanup_directory(settings.FRAME_OUTPUT_DIR)
        raise VideoGenerationError(f"Video generation failed: {str(e)}")