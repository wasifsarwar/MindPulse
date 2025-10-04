"""Helper utility functions."""

import uuid
import re
from typing import Optional


def create_session_id() -> str:
    """
    Create a unique session ID.
    
    Returns:
        UUID string for session identification
    """
    return str(uuid.uuid4())


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize text by removing excessive whitespace and optionally truncating.
    
    Args:
        text: Text to sanitize
        max_length: Optional maximum length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text


def extract_keywords(text: str, min_length: int = 3) -> list:
    """
    Extract keywords from text.
    
    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length
        
    Returns:
        List of keywords
    """
    # Remove punctuation and split
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter by length
    keywords = [w for w in words if len(w) >= min_length]
    
    return keywords


def format_conversation_history(history: list, max_messages: int = 5) -> str:
    """
    Format conversation history for display or processing.
    
    Args:
        history: List of message dictionaries
        max_messages: Maximum number of messages to include
        
    Returns:
        Formatted string
    """
    if not history:
        return "No conversation history"
    
    # Take last N messages
    recent = history[-max_messages:]
    
    formatted = []
    for msg in recent:
        role = msg.get('role', 'unknown').upper()
        content = msg.get('content', '')
        formatted.append(f"{role}: {content}")
    
    return "\n".join(formatted)


def is_crisis_message(text: str) -> bool:
    """
    Detect if a message indicates a mental health crisis.
    
    Args:
        text: Message text
        
    Returns:
        True if crisis indicators are detected
    """
    crisis_keywords = [
        'suicide', 'kill myself', 'end my life', 'want to die',
        'self harm', 'hurt myself', 'no reason to live',
        'better off dead', 'end it all'
    ]
    
    text_lower = text.lower()
    
    return any(keyword in text_lower for keyword in crisis_keywords)


def get_crisis_resources() -> dict:
    """
    Get mental health crisis resources.
    
    Returns:
        Dictionary of crisis resources
    """
    return {
        "national_suicide_prevention_lifeline": {
            "phone": "988 or 1-800-273-8255",
            "description": "24/7 free and confidential support"
        },
        "crisis_text_line": {
            "text": "HOME to 741741",
            "description": "24/7 crisis support via text"
        },
        "international_association_for_suicide_prevention": {
            "website": "https://www.iasp.info/resources/Crisis_Centres/",
            "description": "International crisis center directory"
        },
        "emergency": {
            "phone": "911 (US) or local emergency number",
            "description": "For immediate life-threatening emergencies"
        }
    }

