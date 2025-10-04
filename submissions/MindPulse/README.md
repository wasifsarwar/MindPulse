# MindPulse - AI-Powered Mental Health Support System

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Web Application                       │
│                    (Frontend - Requests)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Server                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Endpoints:                                           │   │
│  │  - /api/chat (mental health conversation)            │   │
│  │  - /api/analyze-sentiment (sentiment analysis)       │   │
│  │  - /api/diagnose (diagnosis insights)                │   │
│  │  - /api/health (health check)                        │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Claude Agent (AI Orchestrator)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  - Uses Anthropic Claude API                         │   │
│  │  - Context-aware conversations                       │   │
│  │  - Retrieves relevant data from datasets             │   │
│  │  - Applies prompt engineering templates              │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Processing Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dataset 1   │  │  Dataset 2   │  │  Dataset 3   │      │
│  │  Counseling  │  │  Sentiment   │  │  Diagnosis   │      │
│  │  Convos      │  │  Analysis    │  │  & Treatment │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Dataset Overview

1. **Mental Health Counseling Conversations** - Context-response pairs from therapy sessions
2. **Sentiment Analysis for Mental Health** - Labeled sentiment data for mental health text
3. **Mental Health Diagnosis and Treatment Monitoring** - Medical diagnosis and treatment tracking

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Anthropic API Key (for Claude)
- Kaggle account for dataset downloads

### Installation

1. Clone the repository and navigate to the project:
```bash
cd /path/to/MindPulse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. Download the datasets:
```bash
# Dataset 1 is already present in dataset/mentalHealthCounselingConversations/
# Download datasets 2 and 3 from Kaggle and place them in dataset/ folder
```

5. Run the FastAPI server:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## 📁 Project Structure

```
MindPulse/
├── main.py                          # Application entry point
├── config.py                        # Configuration settings
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── README.md                        # This file
│
├── api/
│   ├── __init__.py
│   └── routes.py                    # FastAPI endpoint definitions
│
├── agents/
│   ├── __init__.py
│   └── claude_agent.py              # Claude AI agent wrapper
│
├── data_loaders/
│   ├── __init__.py
│   ├── counseling_loader.py         # Dataset 1 loader
│   ├── sentiment_loader.py          # Dataset 2 loader
│   └── diagnosis_loader.py          # Dataset 3 loader
│
├── prompts/
│   ├── __init__.py
│   ├── system_prompts.py            # System-level prompts
│   └── templates.py                 # Prompt templates
│
├── utils/
│   ├── __init__.py
│   ├── vector_store.py              # Vector storage for RAG
│   └── helpers.py                   # Utility functions
│
└── dataset/
    ├── mentalHealthCounselingConversations/
    ├── sentiment_analysis/          # Place dataset 2 here
    └── diagnosis_treatment/         # Place dataset 3 here
```

## 🔧 API Endpoints

### 1. Chat Endpoint
**POST** `/api/chat`
```json
{
  "message": "I've been feeling really anxious lately",
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "response": "I understand that anxiety can be overwhelming...",
  "session_id": "session-123",
  "context_used": ["counseling_data"],
  "sentiment": "negative"
}
```

### 2. Sentiment Analysis
**POST** `/api/analyze-sentiment`
```json
{
  "text": "I feel hopeless and can't sleep"
}
```

Response:
```json
{
  "sentiment": "negative",
  "confidence": 0.87,
  "emotions": ["sadness", "anxiety"],
  "severity": "moderate"
}
```

### 3. Diagnosis Insights
**POST** `/api/diagnose`
```json
{
  "symptoms": ["insomnia", "loss of appetite", "fatigue"],
  "duration": "2 weeks"
}
```

Response:
```json
{
  "insights": "Based on patterns in the data...",
  "similar_cases": 45,
  "recommendations": ["Seek professional help", "..."]
}
```

### 4. Health Check
**GET** `/api/health`

Response:
```json
{
  "status": "healthy",
  "datasets_loaded": true,
  "claude_available": true
}
```

## 🧠 How It Works

### 1. **User Request Flow**
   - Web app sends request to FastAPI
   - FastAPI validates and routes to appropriate endpoint
   - Request data is passed to Claude Agent

### 2. **Claude Agent Processing**
   - Agent analyzes user input
   - Determines which datasets are relevant
   - Queries data loaders for context
   - Constructs prompt with system instructions + context + user query
   - Sends to Claude API

### 3. **Data Retrieval**
   - Data loaders search relevant datasets
   - Use semantic search (vector embeddings) for similarity
   - Return top-k most relevant examples
   - Context is added to Claude's prompt

### 4. **Response Generation**
   - Claude generates empathetic, informed response
   - Response includes citations from datasets
   - Includes confidence scores and sentiment analysis
   - Returns structured JSON to web app

## 🔐 Security & Privacy

- No user data is stored permanently
- Session IDs are temporary (in-memory only)
- API key stored in environment variables
- CORS configured for your frontend domain
- Rate limiting enabled

## 🎯 Key Features

1. **Context-Aware Responses**: Uses historical counseling data to provide informed guidance
2. **Sentiment Analysis**: Real-time emotion detection in user messages
3. **Multi-Dataset Intelligence**: Combines insights from 3 specialized datasets
4. **Session Management**: Maintains conversation context
5. **RAG (Retrieval-Augmented Generation)**: Retrieves relevant examples before responding

## 📝 Environment Variables

Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_api_key_here
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
LOG_LEVEL=INFO
MAX_CONTEXT_EXAMPLES=5
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## 🧪 Testing

```bash
# Test the API
python -m pytest tests/

# Manual testing
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I feel anxious"}'
```

## 📚 Additional Resources

- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Mental Health Data Ethics](https://www.nimh.nih.gov/)

## ⚠️ Disclaimer

This system is for educational/hackathon purposes and should NOT replace professional mental health services. Always encourage users to seek help from licensed professionals for serious mental health concerns.

