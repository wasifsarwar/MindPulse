"""Configuration settings for MindPulse application."""

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # FastAPI Settings
    fastapi_host: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
    fastapi_port: int = int(os.getenv("FASTAPI_PORT", "8000"))
    fastapi_reload: bool = os.getenv("FASTAPI_RELOAD", "True").lower() == "true"
    
    # CORS Settings
    allowed_origins: List[str] = os.getenv(
        "ALLOWED_ORIGINS", 
        "http://localhost:3000,http://localhost:5173"
    ).split(",")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # AI Configuration
    max_context_examples: int = int(os.getenv("MAX_CONTEXT_EXAMPLES", "5"))
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2048"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Embedding Model
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", 
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Session Configuration
    session_timeout_minutes: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    
    # Dataset Paths
    dataset_dir: Path = BASE_DIR / "dataset"
    counseling_data_path: Path = dataset_dir / "mentalHealthCounselingConversations" / "combined_dataset.json"
    sentiment_data_path: Path = dataset_dir / "sentiment_analysis"
    diagnosis_data_path: Path = dataset_dir / "diagnosis_treatment"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Validate critical settings
def validate_settings():
    """Validate that critical settings are properly configured."""
    if not settings.anthropic_api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY is not set. Please add it to your .env file."
        )
    
    if not settings.counseling_data_path.exists():
        raise FileNotFoundError(
            f"Counseling dataset not found at {settings.counseling_data_path}"
        )


if __name__ == "__main__":
    # Test configuration
    validate_settings()
    print("✅ Configuration validated successfully!")
    print(f"📊 Dataset directory: {settings.dataset_dir}")
    print(f"🤖 Claude model: {settings.claude_model}")
    print(f"🌐 API host: {settings.fastapi_host}:{settings.fastapi_port}")

