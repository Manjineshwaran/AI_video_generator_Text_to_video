# Text-to-Video Generator - Backend

## 🏗 AI Architecture Overview

Text Prompt → Image Generation → Transition Creation → Video Compilation

This project approaches text-to-video generation by first using Stable Diffusion to create key frames from text prompts, then blending these images with smooth transitions using PIL, and finally compiling them into a video with OpenCV. The implementation emphasizes modularity, error handling, and configurable output settings (duration, frame rate). The solution balances simplicity with extensibility, providing a foundation that could easily be enhanced with parallel processing, advanced transitions, or additional post-production features.

## 🏗 Architecture Overview

The backend is built using a modern, scalable, and maintainable architecture following these principles:

- **FastAPI** for high-performance API endpoints
- **Modular Design** with clear separation of concerns
- **Asynchronous Processing** for video generation tasks
- **RESTful API** design principles
- **Environment-based Configuration** for different deployment scenarios

## 🚀 Tech Stack

### Core Technologies
- **Python 3.8+** - Primary programming language
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **FFmpeg** - For video processing and manipulation
- **OpenAI DALL·E** - For image generation from text prompts
- **MoviePy** - For video editing and composition

### Development Tools
- **Pytest** - For testing
- **Black & isort** - Code formatting
- **Mypy** - Static type checking
- **Pylint** - Code quality

## 🛠 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration settings
│   │   ├── exceptions.py  # Custom exceptions
│   │   └── logger.py      # Logging configuration
│   │
│   ├── models/            # Data models and schemas
│   │   └── schemas.py     # Pydantic models for request/response
│   │
│   ├── services/          # Business logic
│   │   └── video_service.py # Video generation service
│   │
│   └── utils/             # Utility functions
│       ├── file_utils.py  # File handling utilities
│       └── video_utils.py # Video processing utilities
│
├── static/                # Generated videos and static files
│   └── videos/            # Video storage
│
├── tests/                 # Test files
├── .env.example           # Example environment variables
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- FFmpeg installed and added to system PATH
- OpenAI API key (for DALL·E integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/text-to-video-generator.git
   cd text-to-video-generator/backend
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Docs (Swagger UI):** `http://localhost:8000/docs`
- **Alternative API Docs (ReDoc):** `http://localhost:8000/redoc`

## 🔧 API Endpoints

### Video Generation
- `POST /generate-video`
  - Generate a video from a text prompt
  - **Request Body:**
    ```json
    {
      "prompt": "A beautiful sunset over mountains",
      "duration": 5,
      "fps": 24
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Video generated successfully",
      "video_path": "filename.mp4",
      "download_url": "/download-video?path=filename.mp4"
    }
    ```

### Video Download
- `GET /download-video`
  - Download a generated video
  - **Query Parameters:**
    - `path`: Path to the video file
    - `download`: Set to `true` to force download

### Video Streaming
- `GET /stream-video/{filename}`
  - Stream a video for playback in browser

### List Videos
- `GET /list-videos`
  - List all generated videos
  - **Response:**
    ```json
    {
      "videos": ["video1.mp4", "video2.mp4"]
    }
    ```

## 🧪 Testing

Run tests using pytest:

```bash
pytest tests/
```

## 🛠 Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints for better code documentation
- Keep functions small and focused

### Pre-commit Hooks
Install pre-commit hooks for code quality:

```bash
pre-commit install
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 📧 Contact

Manjineshwaran - [your.email@example.com](mailto:your.email@example.com)

Project Link: [https://github.com/yourusername/text-to-video-generator](https://github.com/yourusername/text-to-video-generator)