"""FastAPI routes for MindPulse API."""

import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

from config import settings
from agents import ClaudeAgent
from data_loaders import CounselingDataLoader, SentimentDataLoader, DiagnosisDataLoader


# Pydantic models for request/response
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User's message")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation continuity")
    use_rag: bool = Field(True, description="Whether to use retrieval-augmented generation")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    session_id: str
    sentiment: dict
    context_used: bool
    num_examples_retrieved: int


class SentimentRequest(BaseModel):
    """Request model for sentiment analysis."""
    text: str = Field(..., description="Text to analyze")


class SentimentResponse(BaseModel):
    """Response model for sentiment analysis."""
    sentiment: str
    confidence: float = 0.0
    primary_emotions: List[str] = []
    severity: Optional[str] = None
    risk_level: Optional[str] = None
    explanation: Optional[str] = None


class DiagnosisRequest(BaseModel):
    """Request model for diagnosis insights."""
    symptoms: List[str] = Field(..., description="List of symptoms")
    duration: str = Field(..., description="How long symptoms have persisted")
    additional_info: Optional[str] = Field(None, description="Additional context")


class DiagnosisResponse(BaseModel):
    """Response model for diagnosis insights."""
    insights: str
    similar_cases_found: int
    symptoms_analyzed: List[str]
    duration: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    claude_available: bool
    datasets_loaded: dict
    active_sessions: int


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="MindPulse API",
        description="AI-powered mental health support system using Claude",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize data loaders and agent
    logger.info("🚀 Initializing MindPulse API...")
    
    try:
        # Load datasets
        counseling_loader = CounselingDataLoader(settings.counseling_data_path)
        sentiment_loader = SentimentDataLoader(settings.sentiment_data_path)
        diagnosis_loader = DiagnosisDataLoader(settings.diagnosis_data_path)
        
        # Initialize embeddings model
        embeddings_model = None
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embeddings model: {settings.embedding_model}")
            embeddings_model = SentenceTransformer(settings.embedding_model)
            logger.info("✅ Embeddings model loaded")
        except Exception as e:
            logger.warning(f"⚠️ Could not load embeddings model: {e}")
            logger.info("RAG will use keyword-based search as fallback")
        
        # Initialize Claude agent
        agent = ClaudeAgent(
            counseling_loader=counseling_loader,
            sentiment_loader=sentiment_loader,
            diagnosis_loader=diagnosis_loader,
            embeddings_model=embeddings_model
        )
        
        # Store in app state
        app.state.agent = agent
        app.state.counseling_loader = counseling_loader
        app.state.sentiment_loader = sentiment_loader
        app.state.diagnosis_loader = diagnosis_loader
        
        logger.info("✅ MindPulse API initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize API: {e}")
        raise
    
    # Routes
    
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "MindPulse API",
            "version": "1.0.0",
            "description": "AI-powered mental health support system",
            "endpoints": {
                "chat": "/api/chat",
                "sentiment": "/api/analyze-sentiment",
                "diagnosis": "/api/diagnose",
                "health": "/api/health"
            },
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc"
            }
        }
    
    @app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
    async def chat(request: ChatRequest):
        """
        Chat with the AI mental health support assistant.
        
        This endpoint provides empathetic, evidence-based guidance using
        Claude AI and relevant examples from counseling conversations.
        """
        try:
            # Generate session ID if not provided
            session_id = request.session_id or str(uuid.uuid4())
            
            # Get response from agent
            result = app.state.agent.chat(
                message=request.message,
                session_id=session_id,
                use_rag=request.use_rag
            )
            
            return ChatResponse(
                response=result.get("response", ""),
                session_id=result.get("session_id", session_id),
                sentiment=result.get("sentiment", {}),
                context_used=result.get("context_used", False),
                num_examples_retrieved=result.get("num_examples_retrieved", 0)
            )
            
        except Exception as e:
            logger.error(f"Error in chat endpoint: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/analyze-sentiment", response_model=SentimentResponse, tags=["Analysis"])
    async def analyze_sentiment(request: SentimentRequest):
        """
        Analyze sentiment and emotional content of text.
        
        This endpoint identifies emotional states, sentiment polarity,
        and potential risk indicators in user messages.
        """
        try:
            result = app.state.agent.analyze_sentiment(request.text)
            
            return SentimentResponse(
                sentiment=result.get("sentiment", "unknown"),
                confidence=result.get("confidence", 0.0),
                primary_emotions=result.get("primary_emotions", []),
                severity=result.get("severity"),
                risk_level=result.get("risk_level"),
                explanation=result.get("explanation")
            )
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis endpoint: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/diagnose", response_model=DiagnosisResponse, tags=["Diagnosis"])
    async def get_diagnosis_insights(request: DiagnosisRequest):
        """
        Get insights and information about symptoms.
        
        This endpoint provides educational information about symptom patterns,
        similar cases, and general guidance. It does NOT provide medical diagnoses.
        """
        try:
            result = app.state.agent.get_diagnosis_insights(
                symptoms=request.symptoms,
                duration=request.duration,
                additional_info=request.additional_info
            )
            
            return DiagnosisResponse(
                insights=result.get("insights", ""),
                similar_cases_found=result.get("similar_cases_found", 0),
                symptoms_analyzed=result.get("symptoms_analyzed", request.symptoms),
                duration=result.get("duration", request.duration)
            )
            
        except Exception as e:
            logger.error(f"Error in diagnosis endpoint: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/health", response_model=HealthResponse, tags=["Health"])
    async def health_check():
        """
        Check the health status of the API and its dependencies.
        
        Returns information about Claude API availability, dataset loading status,
        and active sessions.
        """
        try:
            health_status = app.state.agent.health_check()
            
            return HealthResponse(
                status="healthy" if health_status["claude_available"] else "degraded",
                claude_available=health_status["claude_available"],
                datasets_loaded={
                    "counseling": health_status["counseling_data_loaded"],
                    "sentiment": health_status["sentiment_data_loaded"],
                    "diagnosis": health_status["diagnosis_data_loaded"]
                },
                active_sessions=health_status["active_sessions"]
            )
            
        except Exception as e:
            logger.error(f"Error in health check: {e}")
            return HealthResponse(
                status="unhealthy",
                claude_available=False,
                datasets_loaded={
                    "counseling": False,
                    "sentiment": False,
                    "diagnosis": False
                },
                active_sessions=0
            )
    
    @app.delete("/api/session/{session_id}", tags=["Session"])
    async def clear_session(session_id: str):
        """
        Clear a session's conversation history.
        
        This endpoint removes all conversation history for a given session ID.
        """
        try:
            app.state.agent.clear_session(session_id)
            return {"message": f"Session {session_id} cleared successfully"}
        except Exception as e:
            logger.error(f"Error clearing session: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/session/{session_id}", tags=["Session"])
    async def get_session_history(session_id: str):
        """
        Get conversation history for a session.
        
        Returns all messages in the specified session.
        """
        try:
            history = app.state.agent.get_session_history(session_id)
            return {
                "session_id": session_id,
                "message_count": len(history),
                "history": history
            }
        except Exception as e:
            logger.error(f"Error getting session history: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/stats", tags=["Statistics"])
    async def get_statistics():
        """
        Get statistics about the loaded datasets.
        
        Returns information about the number of records, distribution, etc.
        """
        try:
            return {
                "counseling_data": app.state.counseling_loader.get_statistics(),
                "sentiment_data": app.state.sentiment_loader.get_statistics(),
                "diagnosis_data": app.state.diagnosis_loader.get_statistics()
            }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return app

