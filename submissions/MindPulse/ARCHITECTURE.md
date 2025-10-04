# MindPulse Architecture Deep Dive

## 🎯 Overview

MindPulse is designed as a **multi-layered mental health support system** that uses Claude AI as the foundational model with Retrieval-Augmented Generation (RAG) to provide context-aware, empathetic mental health guidance.

## 🏗️ System Architecture

### Layer 1: Client Layer (Your Web Application)
- **Purpose:** User interface for interacting with the system
- **Communication:** HTTP REST API calls to FastAPI server
- **Protocols:** JSON over HTTP/HTTPS
- **Features:**
  - User input collection
  - Response display
  - Session management
  - Crisis resource display

### Layer 2: API Layer (FastAPI)
**File:** `api/routes.py`

- **Purpose:** HTTP endpoint management and request routing
- **Components:**
  - **CORS Middleware:** Handles cross-origin requests from web app
  - **Request Validation:** Pydantic models ensure data integrity
  - **Route Handlers:** Map HTTP requests to agent functions
  - **Error Handling:** Graceful error responses

**Key Endpoints:**
1. `/api/chat` - Main conversation endpoint
2. `/api/analyze-sentiment` - Sentiment analysis
3. `/api/diagnose` - Diagnosis insights
4. `/api/health` - System health check
5. `/api/session/{id}` - Session management

### Layer 3: Agent Layer (Claude Agent)
**File:** `agents/claude_agent.py`

- **Purpose:** Orchestrates AI interactions and decision-making
- **Core Responsibilities:**
  1. **Query Understanding:** Interprets user intent
  2. **Context Retrieval:** Fetches relevant data from datasets
  3. **Prompt Construction:** Builds effective prompts for Claude
  4. **Response Generation:** Calls Claude API
  5. **Session Management:** Tracks conversation history

**Agent Flow:**
```
User Message
    ↓
Intent Analysis
    ↓
Context Retrieval (RAG)
    ↓
Prompt Engineering
    ↓
Claude API Call
    ↓
Response Processing
    ↓
Return to User
```

### Layer 4: Data Layer
**Files:** `data_loaders/*.py`

Three specialized data loaders:

#### 1. CounselingDataLoader
- **Dataset:** Mental Health Counseling Conversations
- **Format:** JSON with Context-Response pairs
- **Use Case:** Provides real counseling examples for RAG
- **Search Methods:**
  - Keyword-based search
  - Semantic similarity (with embeddings)
  - Random sampling

#### 2. SentimentDataLoader
- **Dataset:** Sentiment Analysis for Mental Health
- **Format:** CSV with text and sentiment labels
- **Use Case:** Training data for sentiment understanding
- **Capabilities:**
  - Sentiment distribution analysis
  - Text-based search
  - Label filtering

#### 3. DiagnosisDataLoader
- **Dataset:** Mental Health Diagnosis and Treatment
- **Format:** CSV with symptoms, conditions, treatments
- **Use Case:** Educational information about conditions
- **Capabilities:**
  - Symptom-based search
  - Condition lookup
  - Treatment approach retrieval

### Layer 5: Prompt Engineering Layer
**Files:** `prompts/*.py`

#### System Prompts
Three specialized system prompts:
1. **Mental Health Counselor:** Empathetic guidance
2. **Sentiment Analyzer:** Emotion detection
3. **Diagnosis Assistant:** Educational information

#### Prompt Templates
Dynamic prompt construction:
- `create_chat_prompt()` - Builds conversational prompts with RAG
- `create_sentiment_prompt()` - Structures sentiment analysis
- `create_diagnosis_prompt()` - Formats symptom inquiries

## 🔄 Data Flow Examples

### Example 1: Chat Request

```
1. User sends: "I've been feeling really anxious"
   ↓
2. FastAPI receives POST to /api/chat
   ↓
3. ClaudeAgent.chat() is called
   ↓
4. Agent analyzes message sentiment (pre-check)
   ↓
5. RAG: CounselingDataLoader searches for similar contexts
   - Converts message to embedding
   - Compares with dataset embeddings
   - Returns top 5 similar conversations
   ↓
6. Prompt is constructed:
   - System: Mental Health Counselor prompt
   - Context: 5 relevant counseling examples
   - History: Last 3 messages (if session exists)
   - User: Current message
   ↓
7. Claude API generates response
   ↓
8. Response enriched with metadata
   ↓
9. Session updated with conversation
   ↓
10. JSON response sent to web app
```

### Example 2: Diagnosis Insights

```
1. User provides: symptoms=["insomnia", "fatigue"], duration="2 weeks"
   ↓
2. FastAPI receives POST to /api/diagnose
   ↓
3. ClaudeAgent.get_diagnosis_insights() is called
   ↓
4. DiagnosisDataLoader searches for similar symptom patterns
   - Matches symptoms against database
   - Calculates match scores
   - Returns top 3 similar cases
   ↓
5. Prompt constructed with:
   - System: Diagnosis Assistant prompt
   - Similar cases from dataset
   - Educational guidelines
   - Safety warnings
   ↓
6. Claude generates insights
   ↓
7. Response includes:
   - Educational information
   - Coping strategies
   - Professional help recommendations
   ↓
8. JSON response with insights + metadata
```

## 🧠 RAG (Retrieval-Augmented Generation) Implementation

### Why RAG?
- **Grounding:** Responses based on real counseling data
- **Accuracy:** Reduces hallucinations
- **Context:** Provides relevant examples
- **Learning:** Leverages existing therapeutic knowledge

### How It Works

1. **Indexing Phase** (on startup):
   ```python
   # Convert all counseling conversations to embeddings
   texts = [f"{conv['Context']} {conv['Response']}" for conv in data]
   embeddings = model.encode(texts)
   # Store in memory for fast retrieval
   ```

2. **Retrieval Phase** (per request):
   ```python
   # Convert user query to embedding
   query_embedding = model.encode([user_message])
   
   # Compute similarities
   similarities = cosine_similarity(query_embedding, all_embeddings)
   
   # Get top-k most similar
   top_indices = argsort(similarities)[-k:]
   relevant_contexts = [conversations[i] for i in top_indices]
   ```

3. **Generation Phase**:
   ```python
   # Construct prompt with retrieved contexts
   prompt = f"""
   {SYSTEM_PROMPT}
   
   Relevant Examples:
   {format_contexts(relevant_contexts)}
   
   User Message: {user_message}
   
   Your Response:
   """
   
   # Generate with Claude
   response = claude.messages.create(...)
   ```

## 🔐 Security & Privacy Considerations

### Data Handling
- **No Persistent Storage:** Conversations stored in-memory only
- **Session Expiry:** Sessions cleared after timeout
- **No Logging of User Data:** Logs contain system events, not user messages
- **API Key Security:** Stored in environment variables

### Safety Features
1. **Crisis Detection:** 
   - Keywords monitored in `utils/helpers.py`
   - Automatic crisis resource provision
   
2. **Professional Guidance:**
   - Always recommends seeking professional help
   - Never diagnoses or prescribes
   
3. **Rate Limiting:** Can be added via middleware

## 📊 Performance Optimizations

### 1. Embedding Caching
- Counseling dataset embeddings computed once on startup
- Cached in memory for fast retrieval
- ~3500 conversations × 384-dim vectors = ~5MB RAM

### 2. Session Management
- In-memory dictionary for fast access
- Limited to last 10 messages per session
- Automatic cleanup possible (not implemented in hackathon version)

### 3. Async Operations
- FastAPI handles requests asynchronously
- Multiple users can interact simultaneously
- Non-blocking I/O for API calls

## 🎨 Prompt Engineering Strategy

### Design Principles

1. **Role Definition:** Clearly define Claude's role (counselor, analyzer, educator)
2. **Constraints:** Explicit limitations (no diagnosis, no prescription)
3. **Context Provision:** Relevant examples from datasets
4. **Output Format:** Structured responses for consistency
5. **Safety First:** Crisis resources and professional referrals

### Template Structure

```
[SYSTEM PROMPT]
- Role and responsibilities
- Guidelines and constraints
- Tone and style requirements

[CONTEXT]
- Retrieved examples from RAG
- Conversation history
- Similar cases

[USER INPUT]
- Current message/query
- Structured information

[OUTPUT SPECIFICATION]
- Desired format
- Required elements
- Safety reminders
```

## 🔄 Session Management

### In-Memory Storage
```python
sessions = {
    "session-uuid-123": [
        {"role": "user", "content": "I feel anxious"},
        {"role": "assistant", "content": "I understand..."},
        ...
    ]
}
```

### Session Lifecycle
1. **Creation:** On first message or explicit session_id
2. **Update:** After each message exchange
3. **Retrieval:** For context in subsequent messages
4. **Cleanup:** Manual via API or on server restart

### Future Enhancements
- Persistent storage (Redis, PostgreSQL)
- Automatic expiry
- User authentication
- Session migration

## 🚀 Scaling Considerations

### Current Limitations (Hackathon Version)
- In-memory data storage
- Single-server deployment
- No load balancing
- No persistent sessions

### Production-Ready Enhancements

1. **Database Integration:**
   - Vector DB (Pinecone, Weaviate) for embeddings
   - PostgreSQL for structured data
   - Redis for session caching

2. **Horizontal Scaling:**
   - Multiple FastAPI instances
   - Load balancer (Nginx, HAProxy)
   - Shared session store

3. **Monitoring:**
   - Prometheus metrics
   - Grafana dashboards
   - Error tracking (Sentry)

4. **CI/CD:**
   - Automated testing
   - Docker containers
   - Kubernetes orchestration

## 📈 Extending the System

### Add New Datasets
1. Create new loader in `data_loaders/`
2. Initialize in `api/routes.py`
3. Add to agent's capabilities
4. Update prompts to use new data

### Add New Endpoints
1. Define Pydantic models in `api/routes.py`
2. Create agent method in `agents/claude_agent.py`
3. Add route handler
4. Update documentation

### Customize Prompts
1. Edit system prompts in `prompts/system_prompts.py`
2. Modify templates in `prompts/templates.py`
3. Test with various inputs
4. Iterate based on responses

## 🧪 Testing Strategy

### Unit Tests
- Data loaders
- Helper functions
- Prompt templates

### Integration Tests
- Agent + Data loaders
- API endpoints
- End-to-end flows

### Manual Testing
- Use `test_api.py`
- Interactive docs at `/docs`
- Real user scenarios

## 📚 Key Technologies

- **FastAPI:** Modern, async Python web framework
- **Claude (Anthropic):** State-of-the-art language model
- **Sentence Transformers:** Semantic embeddings
- **Pandas:** Data processing
- **Pydantic:** Data validation
- **Uvicorn:** ASGI server
- **Loguru:** Elegant logging

## 💡 Design Philosophy

1. **Empathy First:** Every response prioritizes user well-being
2. **Evidence-Based:** Grounded in real counseling data
3. **Safety Critical:** Never replaces professional help
4. **Transparent:** Clear about limitations
5. **Accessible:** Easy to use and understand
6. **Extensible:** Modular design for easy enhancements

---

This architecture provides a solid foundation for a mental health support system while maintaining ethical standards and user safety.

