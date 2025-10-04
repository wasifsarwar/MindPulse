"""Claude AI Agent for MindPulse - handles all AI interactions."""

import json
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from loguru import logger

from config import settings
from prompts import (
    MENTAL_HEALTH_COUNSELOR_PROMPT,
    SENTIMENT_ANALYZER_PROMPT,
    DIAGNOSIS_ASSISTANT_PROMPT,
    create_chat_prompt,
    create_sentiment_prompt,
    create_diagnosis_prompt,
    create_rag_context
)


class ClaudeAgent:
    """
    Claude-powered AI agent for mental health support.
    
    This agent handles all interactions with Claude API and manages
    different types of mental health-related queries.
    """
    
    def __init__(
        self,
        counseling_loader=None,
        sentiment_loader=None,
        diagnosis_loader=None,
        embeddings_model=None
    ):
        """
        Initialize the Claude agent.
        
        Args:
            counseling_loader: Counseling data loader
            sentiment_loader: Sentiment data loader
            diagnosis_loader: Diagnosis data loader
            embeddings_model: Sentence transformer model for RAG
        """
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.counseling_loader = counseling_loader
        self.sentiment_loader = sentiment_loader
        self.diagnosis_loader = diagnosis_loader
        self.embeddings_model = embeddings_model
        
        # Session management (in-memory for hackathon)
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        
        logger.info("✅ Claude Agent initialized")
    
    def chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        use_rag: bool = True
    ) -> Dict[str, Any]:
        """
        Handle a chat message from the user.
        
        Args:
            message: User's message
            session_id: Optional session ID for conversation continuity
            use_rag: Whether to use RAG (Retrieval-Augmented Generation)
            
        Returns:
            Response dictionary with message, sentiment, and metadata
        """
        try:
            logger.info(f"Processing chat message: {message[:50]}...")
            
            # Get conversation history
            conversation_history = []
            if session_id and session_id in self.sessions:
                conversation_history = self.sessions[session_id]
            
            # Retrieve relevant context using RAG
            context_examples = []
            if use_rag and self.counseling_loader:
                context_examples = self.counseling_loader.search_by_similarity(
                    query=message,
                    embeddings_model=self.embeddings_model,
                    max_results=settings.max_context_examples
                )
                logger.info(f"Retrieved {len(context_examples)} relevant examples")
            
            # Create the prompt
            user_prompt = create_chat_prompt(
                user_message=message,
                context_examples=context_examples,
                conversation_history=conversation_history
            )
            
            # Call Claude API
            response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
                system=MENTAL_HEALTH_COUNSELOR_PROMPT,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Extract response text
            assistant_message = response.content[0].text
            
            # Analyze sentiment of user message
            sentiment_info = self.analyze_sentiment(message)
            
            # Update conversation history
            if session_id:
                if session_id not in self.sessions:
                    self.sessions[session_id] = []
                
                self.sessions[session_id].append({
                    "role": "user",
                    "content": message
                })
                self.sessions[session_id].append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                # Keep only last 10 messages
                if len(self.sessions[session_id]) > 10:
                    self.sessions[session_id] = self.sessions[session_id][-10:]
            
            return {
                "response": assistant_message,
                "session_id": session_id,
                "sentiment": sentiment_info,
                "context_used": len(context_examples) > 0,
                "num_examples_retrieved": len(context_examples)
            }
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again or seek immediate help if you're in crisis. National Suicide Prevention Lifeline: 988",
                "error": str(e),
                "session_id": session_id
            }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment and emotional content of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis results
        """
        try:
            logger.info(f"Analyzing sentiment for: {text[:50]}...")
            
            # Create sentiment prompt
            sentiment_prompt = create_sentiment_prompt(text)
            
            # Call Claude API
            response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=1024,
                temperature=0.3,  # Lower temperature for more consistent analysis
                system=SENTIMENT_ANALYZER_PROMPT,
                messages=[
                    {"role": "user", "content": sentiment_prompt}
                ]
            )
            
            # Parse response
            result_text = response.content[0].text
            
            # Try to extract JSON from response
            try:
                # Find JSON in the response
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = result_text[start_idx:end_idx]
                    sentiment_data = json.loads(json_str)
                    return sentiment_data
                else:
                    # Fallback if no JSON found
                    return {
                        "sentiment": "neutral",
                        "confidence": 0.5,
                        "explanation": result_text
                    }
            except json.JSONDecodeError:
                logger.warning("Could not parse sentiment JSON, using fallback")
                return {
                    "sentiment": "neutral",
                    "confidence": 0.5,
                    "explanation": result_text
                }
                
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                "sentiment": "unknown",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def get_diagnosis_insights(
        self,
        symptoms: List[str],
        duration: str,
        additional_info: str = None
    ) -> Dict[str, Any]:
        """
        Get insights about symptoms and potential conditions.
        
        Args:
            symptoms: List of symptoms
            duration: How long symptoms have persisted
            additional_info: Any additional context
            
        Returns:
            Insights and recommendations
        """
        try:
            logger.info(f"Getting diagnosis insights for symptoms: {symptoms}")
            
            # Search for similar cases
            similar_cases = []
            if self.diagnosis_loader:
                similar_cases = self.diagnosis_loader.search_by_symptoms(
                    symptoms=symptoms,
                    max_results=3
                )
                logger.info(f"Found {len(similar_cases)} similar cases")
            
            # Create diagnosis prompt
            diagnosis_prompt = create_diagnosis_prompt(
                symptoms=symptoms,
                duration=duration,
                additional_info=additional_info,
                similar_cases=similar_cases
            )
            
            # Call Claude API
            response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
                system=DIAGNOSIS_ASSISTANT_PROMPT,
                messages=[
                    {"role": "user", "content": diagnosis_prompt}
                ]
            )
            
            insights_text = response.content[0].text
            
            return {
                "insights": insights_text,
                "similar_cases_found": len(similar_cases),
                "similar_cases": similar_cases[:2],  # Return first 2 for reference
                "symptoms_analyzed": symptoms,
                "duration": duration
            }
            
        except Exception as e:
            logger.error(f"Error getting diagnosis insights: {e}")
            return {
                "insights": "I apologize, but I'm unable to provide insights at this time. Please consult with a healthcare professional for proper evaluation.",
                "error": str(e)
            }
    
    def analyze_survey(
        self,
        medication_taken: bool,
        mood_rating: int,
        sleep_quality: int,
        physical_activity: int,
        thoughts: str
    ) -> Dict[str, Any]:
        """
        Analyze daily survey responses and provide empathetic support.
        
        Args:
            medication_taken: Whether medication was taken
            mood_rating: Mood rating 1-10
            sleep_quality: Sleep quality 1-10
            physical_activity: Activity level 1-10
            thoughts: User's thoughts/feelings
            
        Returns:
            Empathetic message with recommendations
        """
        try:
            logger.info(f"Analyzing survey: mood={mood_rating}, sleep={sleep_quality}, activity={physical_activity}")
            
            # === FIRST: Detect deterioration based on hard rules (don't rely on Claude) ===
            from utils.sms import is_deterioration_detected, send_provider_alert
            
            # Determine risk level and concerns based on actual values
            determined_concerns = []
            if not medication_taken:
                determined_concerns.append("missed_medication")
            if mood_rating <= 3:
                determined_concerns.append("low_mood")
            if sleep_quality <= 3:
                determined_concerns.append("poor_sleep")
            if physical_activity <= 2:
                determined_concerns.append("minimal_activity")
            
            # Calculate risk level based on factors
            concern_count = len(determined_concerns)
            if concern_count >= 3 or (not medication_taken and mood_rating <= 3):
                determined_risk = "high"
            elif concern_count >= 2:
                determined_risk = "moderate"
            else:
                determined_risk = "low"
            
            # Check if we should alert provider
            provider_contacted = False
            deterioration_detected = is_deterioration_detected(
                medication_taken,
                mood_rating,
                sleep_quality,
                physical_activity,
                determined_risk
            )
            
            if deterioration_detected:
                logger.warning(f"⚠️ Mental health deterioration detected - Risk: {determined_risk}, Concerns: {determined_concerns}")
                
                # Always mark as contacted for UI notification (even if SMS disabled for demo)
                provider_contacted = True
                
                # Try to send actual SMS alert
                send_provider_alert(
                    patient_info="Survey respondent",
                    concern_level=determined_risk,
                    key_concerns=determined_concerns
                )
            
            # === NOW: Get empathetic message from Claude ===
            # Build a simple prompt
            prompt = f"""A person has shared their daily check-in:

- Medication taken today: {"Yes" if medication_taken else "No"}
- Mood rating (1-10): {mood_rating}
- Sleep quality (1-10): {sleep_quality}
- Physical activity (1-10): {physical_activity}
- What's on their mind: "{thoughts}"

Please provide:
1. An empathetic, warm response (2-3 sentences) acknowledging how they're doing
2. 2-3 simple, actionable recommendations based on their responses
3. Identify any key concerns (like low mood, poor sleep, missed medication)
4. Risk level: low, moderate, or high

Be compassionate, understanding, and encouraging. Keep it simple and supportive.

Return your response in this format:
MESSAGE: [Your empathetic message here]
RECOMMENDATIONS: 
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]
KEY_CONCERNS: [concern1, concern2]
RISK_LEVEL: [low/moderate/high]
"""
            
            # Call Claude
            response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=800,
                temperature=0.7,
                system="You are a compassionate mental health support assistant. Provide warm, empathetic responses focused on practical support.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.content[0].text
            
            # Parse response (simple parsing)
            message = ""
            recommendations = []
            key_concerns = []
            risk_level = "low"
            
            lines = result_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith("MESSAGE:"):
                    message = line.replace("MESSAGE:", "").strip()
                    current_section = "message"
                elif line.startswith("RECOMMENDATIONS:"):
                    current_section = "recommendations"
                elif line.startswith("KEY_CONCERNS:"):
                    concerns_text = line.replace("KEY_CONCERNS:", "").strip()
                    key_concerns = [c.strip() for c in concerns_text.split(",") if c.strip()]
                    current_section = None
                elif line.startswith("RISK_LEVEL:"):
                    risk_level = line.replace("RISK_LEVEL:", "").strip().lower()
                    current_section = None
                elif current_section == "recommendations" and line.startswith("-"):
                    recommendations.append(line.replace("-", "").strip())
                elif current_section == "message" and line and not line.startswith(("RECOMMENDATIONS", "KEY_CONCERNS", "RISK_LEVEL")):
                    message += " " + line
            
            # Fallback if parsing fails
            if not message:
                message = result_text[:200]
            if not recommendations:
                recommendations = ["Take things one step at a time", "Reach out to someone you trust if you need support"]
            
            # Use Claude's concerns if available, otherwise use our determined ones
            if not key_concerns:
                key_concerns = determined_concerns
            
            # Use Claude's risk level if valid, otherwise use our determined one
            if risk_level not in ["low", "moderate", "high"]:
                risk_level = determined_risk
            
            return {
                "message": message.strip(),
                "recommendations": recommendations[:3],
                "risk_level": risk_level,
                "key_concerns": key_concerns[:3],
                "provider_contacted": provider_contacted
            }
            
        except Exception as e:
            logger.error(f"Error analyzing survey: {e}")
            return {
                "message": "Thank you for sharing. Remember, it's okay to have ups and downs. You're taking a positive step by checking in with yourself.",
                "recommendations": [
                    "Take things one day at a time",
                    "Reach out to someone you trust if you need support",
                    "Consider speaking with a mental health professional"
                ],
                "risk_level": "moderate",
                "key_concerns": [],
                "provider_contacted": False,
                "error": str(e)
            }
    
    def clear_session(self, session_id: str):
        """
        Clear a session's conversation history.
        
        Args:
            session_id: Session ID to clear
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleared session: {session_id}")
    
    def get_session_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of messages in the session
        """
        return self.sessions.get(session_id, [])
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the agent and its dependencies are healthy.
        
        Returns:
            Health status information
        """
        health_status = {
            "claude_available": False,
            "counseling_data_loaded": False,
            "sentiment_data_loaded": False,
            "diagnosis_data_loaded": False,
            "embeddings_available": self.embeddings_model is not None,
            "active_sessions": len(self.sessions)
        }
        
        # Check Claude API
        try:
            test_response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            health_status["claude_available"] = True
        except Exception as e:
            logger.error(f"Claude API health check failed: {e}")
        
        # Check data loaders
        if self.counseling_loader:
            stats = self.counseling_loader.get_statistics()
            health_status["counseling_data_loaded"] = stats["total_conversations"] > 0
        
        if self.sentiment_loader:
            stats = self.sentiment_loader.get_statistics()
            health_status["sentiment_data_loaded"] = stats["total_records"] > 0
        
        if self.diagnosis_loader:
            stats = self.diagnosis_loader.get_statistics()
            health_status["diagnosis_data_loaded"] = stats["total_records"] > 0
        
        return health_status

