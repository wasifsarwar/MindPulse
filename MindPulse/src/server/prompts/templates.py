"""Prompt templates for different use cases."""

from typing import List, Dict, Any


def create_chat_prompt(
    user_message: str, 
    context_examples: List[Dict[str, str]], 
    conversation_history: List[Dict[str, str]] = None
) -> str:
    """
    Create a chat prompt with context from counseling dataset.
    
    Args:
        user_message: The user's current message
        context_examples: Relevant examples from counseling dataset
        conversation_history: Previous messages in this session
        
    Returns:
        Formatted prompt string
    """
    prompt_parts = []
    
    # Add conversation history if available
    if conversation_history:
        prompt_parts.append("**Previous Conversation:**")
        for msg in conversation_history[-3:]:  # Last 3 messages for context
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt_parts.append(f"{role.upper()}: {content}")
        prompt_parts.append("")
    
    # Add relevant context examples
    if context_examples:
        prompt_parts.append("**Relevant Context from Counseling Data:**")
        for i, example in enumerate(context_examples[:3], 1):  # Top 3 examples
            context = example.get("Context", "")
            response = example.get("Response", "")
            prompt_parts.append(f"\nExample {i}:")
            prompt_parts.append(f"User: {context[:200]}...")
            prompt_parts.append(f"Counselor: {response[:200]}...")
        prompt_parts.append("")
    
    # Add current user message
    prompt_parts.append("**Current User Message:**")
    prompt_parts.append(user_message)
    prompt_parts.append("")
    prompt_parts.append("**Your Response:**")
    prompt_parts.append("Provide a compassionate, helpful response that:")
    prompt_parts.append("1. Validates the user's feelings")
    prompt_parts.append("2. Offers supportive guidance")
    prompt_parts.append("3. Suggests practical next steps if appropriate")
    prompt_parts.append("4. Recommends professional help if needed")
    
    return "\n".join(prompt_parts)


def create_sentiment_prompt(text: str, context: str = None) -> str:
    """
    Create a sentiment analysis prompt.
    
    Args:
        text: The text to analyze
        context: Optional additional context
        
    Returns:
        Formatted prompt string
    """
    prompt_parts = [
        "**Text to Analyze:**",
        text,
        "",
        "**Analysis Required:**",
        "Provide a comprehensive sentiment analysis in the following JSON format:",
        "",
        "{",
        '  "sentiment": "positive|negative|neutral|mixed",',
        '  "primary_emotions": ["emotion1", "emotion2", "emotion3"],',
        '  "severity": "mild|moderate|severe",',
        '  "risk_level": "low|moderate|high|critical",',
        '  "confidence": 0.0-1.0,',
        '  "explanation": "Brief explanation of your analysis",',
        '  "risk_indicators": ["any concerning phrases or patterns"],',
        '  "suggested_response_tone": "recommended tone for response"',
        "}"
    ]
    
    if context:
        prompt_parts.insert(2, f"**Additional Context:** {context}")
        prompt_parts.insert(3, "")
    
    return "\n".join(prompt_parts)


def create_diagnosis_prompt(
    symptoms: List[str], 
    duration: str, 
    additional_info: str = None,
    similar_cases: List[Dict[str, Any]] = None
) -> str:
    """
    Create a diagnosis insights prompt.
    
    Args:
        symptoms: List of reported symptoms
        duration: How long symptoms have persisted
        additional_info: Any additional context
        similar_cases: Similar cases from dataset
        
    Returns:
        Formatted prompt string
    """
    prompt_parts = [
        "**Reported Information:**",
        f"Symptoms: {', '.join(symptoms)}",
        f"Duration: {duration}",
    ]
    
    if additional_info:
        prompt_parts.append(f"Additional Context: {additional_info}")
    
    prompt_parts.extend([
        "",
        "**Similar Patterns from Research Data:**"
    ])
    
    if similar_cases:
        for i, case in enumerate(similar_cases[:3], 1):
            prompt_parts.append(f"\nCase {i}:")
            prompt_parts.append(f"  Pattern: {case.get('pattern', 'N/A')}")
            prompt_parts.append(f"  Common Approaches: {case.get('approaches', 'N/A')}")
    else:
        prompt_parts.append("(No directly similar cases found in dataset)")
    
    prompt_parts.extend([
        "",
        "**Your Response Should Include:**",
        "1. Educational information about these symptom patterns",
        "2. Common factors that may contribute to these experiences",
        "3. Evidence-based self-care strategies that may help",
        "4. When and why to seek professional evaluation",
        "5. Types of professionals who can help (therapist, psychiatrist, etc.)",
        "",
        "**Important Reminders:**",
        "- Do NOT provide a diagnosis",
        "- Do NOT prescribe treatment or medication",
        "- DO emphasize the importance of professional evaluation",
        "- DO provide hope and support",
        "",
        "**Your Response:**"
    ])
    
    return "\n".join(prompt_parts)


def create_rag_context(examples: List[Dict[str, Any]], max_length: int = 2000) -> str:
    """
    Create a RAG (Retrieval-Augmented Generation) context from examples.
    
    Args:
        examples: List of relevant examples from datasets
        max_length: Maximum character length for context
        
    Returns:
        Formatted context string
    """
    context_parts = []
    current_length = 0
    
    for i, example in enumerate(examples, 1):
        example_text = f"\n--- Example {i} ---\n"
        
        if "Context" in example and "Response" in example:
            example_text += f"User: {example['Context']}\n"
            example_text += f"Counselor: {example['Response']}\n"
        elif "text" in example and "label" in example:
            example_text += f"Text: {example['text']}\n"
            example_text += f"Sentiment: {example['label']}\n"
        else:
            example_text += str(example) + "\n"
        
        if current_length + len(example_text) > max_length:
            break
            
        context_parts.append(example_text)
        current_length += len(example_text)
    
    return "".join(context_parts)

