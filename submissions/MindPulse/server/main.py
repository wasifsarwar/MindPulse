"""
MindPulse - AI-Powered Mental Health Support System
Main application entry point
"""

import sys
from pathlib import Path
from loguru import logger
import uvicorn

from config import settings, validate_settings
from api import create_app


def setup_logging():
    """Configure logging for the application."""
    logger.remove()  # Remove default handler
    
    # Add console handler with custom format
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True
    )
    
    # Add file handler
    log_path = Path(__file__).parent.parent / "logs" / "mindpulse.log"
    log_path.parent.mkdir(exist_ok=True)
    logger.add(
        str(log_path),
        rotation="500 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"
    )


def main():
    """Main function to run the FastAPI application."""
    # Setup logging
    setup_logging()
    
    logger.info("=" * 60)
    logger.info("🧠 MindPulse - AI-Powered Mental Health Support System")
    logger.info("=" * 60)
    
    # Validate configuration
    try:
        validate_settings()
        logger.info("✅ Configuration validated")
    except Exception as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.error("Please check your .env file and ensure all required settings are configured")
        sys.exit(1)
    
    # Create FastAPI app
    try:
        app = create_app()
        logger.info("✅ FastAPI application created")
    except Exception as e:
        logger.error(f"❌ Failed to create application: {e}")
        sys.exit(1)
    
    # Display startup information
    logger.info("")
    logger.info("🚀 Starting MindPulse API Server")
    logger.info(f"📍 Host: {settings.fastapi_host}")
    logger.info(f"🔌 Port: {settings.fastapi_port}")
    logger.info(f"🤖 Claude Model: {settings.claude_model}")
    logger.info(f"📊 Max Context Examples: {settings.max_context_examples}")
    logger.info("")
    logger.info(f"📖 API Documentation: http://localhost:{settings.fastapi_port}/docs")
    logger.info(f"📘 ReDoc: http://localhost:{settings.fastapi_port}/redoc")
    logger.info("")
    logger.info("⚠️  IMPORTANT: This is for educational/hackathon purposes only.")
    logger.info("    NOT a replacement for professional mental health services.")
    logger.info("")
    logger.info("=" * 60)
    
    # Run the server
    uvicorn.run(
        app,
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        log_level=settings.log_level.lower(),
        access_log=True
    )


if __name__ == "__main__":
    main()

