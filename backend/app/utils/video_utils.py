from typing import List
import os
from PIL import Image
import cv2
import logging

logger = logging.getLogger(__name__)

def generate_transitions(image_paths: List[str], output_dir: str) -> List[str]:
    """Create smooth transitions between frames"""
    try:
        frames = []
        for i in range(len(image_paths)-1):
            try:
                img1 = Image.open(image_paths[i])
                img2 = Image.open(image_paths[i+1])
                frames.append(image_paths[i])
                
                # Create 3 transition frames between each pair
                for t in range(1, 4):
                    blended = Image.blend(img1, img2, t/4)
                    transition_path = os.path.join(output_dir, f"transition_{i:03d}_{t:02d}.png")
                    blended.save(transition_path)
                    frames.append(transition_path)
            except Exception as e:
                logger.error(f"Transition error between frames {i}-{i+1}: {str(e)}", exc_info=True)
                continue
        
        frames.append(image_paths[-1])
        return frames
        
    except Exception as e:
        logger.error(f"Error in transition generation: {str(e)}", exc_info=True)
        raise

def create_video_from_frames(image_paths: List[str], output_file: str, fps: int = 12) -> None:
    """Convert images to video using OpenCV"""
    try:
        if not image_paths:
            raise ValueError("No images provided for video creation")
        
        # Get dimensions from first image
        first_image = cv2.imread(image_paths[0])
        if first_image is None:
            raise ValueError("Could not read the first frame")
        
        height, width, _ = first_image.shape
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        if not video.isOpened():
            raise ValueError("Could not open video writer")
        
        # Write frames to video
        for img_path in image_paths:
            frame = cv2.imread(img_path)
            if frame is not None:
                video.write(frame)
            else:
                logger.warning(f"Could not read frame: {img_path}")
        
        video.release()
        
    except Exception as e:
        logger.error(f"Video creation failed: {str(e)}", exc_info=True)
        raise