"""Prompt engineering module for MindPulse."""

from .system_prompts import (
    MENTAL_HEALTH_COUNSELOR_PROMPT,
    SENTIMENT_ANALYZER_PROMPT,
    DIAGNOSIS_ASSISTANT_PROMPT
)
from .templates import (
    create_chat_prompt,
    create_sentiment_prompt,
    create_diagnosis_prompt
)

__all__ = [
    "MENTAL_HEALTH_COUNSELOR_PROMPT",
    "SENTIMENT_ANALYZER_PROMPT",
    "DIAGNOSIS_ASSISTANT_PROMPT",
    "create_chat_prompt",
    "create_sentiment_prompt",
    "create_diagnosis_prompt",
]

