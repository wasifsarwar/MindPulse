"""Configuration settings for MindPulse application."""

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory (server folder)
BASE_DIR = Path(__file__).parent
# Project root (one level up from server)
PROJECT_ROOT = BASE_DIR.parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    anthropic_api_key: str = "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"
    
    # FastAPI Settings
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    fastapi_reload: bool = True
    
    # CORS Settings
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Logging
    log_level: str = "INFO"
    
    # AI Configuration
    max_context_examples: int = 5
    claude_model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 2048
    temperature: float = 0.7
    
    # Embedding Model
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Session Configuration
    session_timeout_minutes: int = 30
    
    # SMS Configuration (Twilio)
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""
    provider_phone_number: str = ""
    enable_sms_alerts: bool = False
    
    # Dataset Paths (relative to project root)
    dataset_dir: Path = PROJECT_ROOT / "dataset"
    counseling_data_path: Path = dataset_dir / "mentalHealthCounselingConversations" / "combined_dataset.json"
    sentiment_data_path: Path = dataset_dir / "sentiment_analysis"
    diagnosis_data_path: Path = dataset_dir / "diagnosis_treatment"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_allowed_origins_list(self) -> List[str]:
        """Get allowed origins as a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


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

