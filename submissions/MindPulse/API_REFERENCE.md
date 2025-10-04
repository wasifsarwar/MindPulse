# MindPulse API Reference

Complete reference for all API endpoints with examples.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required (hackathon version).

---

## Endpoints

### 1. Root Endpoint

**GET** `/`

Get API information.

**Response:**
```json
{
  "name": "MindPulse API",
  "version": "1.0.0",
  "description": "AI-powered mental health support system",
  "endpoints": {
    "chat": "/api/chat",
    "sentiment": "/api/analyze-sentiment",
    "diagnosis": "/api/diagnose",
    "health": "/api/health"
  }
}
```

---

### 2. Chat Endpoint

**POST** `/api/chat`

Main conversation endpoint for mental health support.

**Request Body:**
```json
{
  "message": "I've been feeling really anxious lately",
  "session_id": "optional-uuid-here",
  "use_rag": true
}
```

**Parameters:**
- `message` (string, required) - User's message
- `session_id` (string, optional) - Session ID for conversation continuity
- `use_rag` (boolean, optional, default: true) - Whether to use RAG

**Response:**
```json
{
  "response": "I hear that you're experiencing anxiety...",
  "session_id": "generated-uuid-123",
  "sentiment": {
    "sentiment": "negative",
    "confidence": 0.85,
    "primary_emotions": ["anxiety", "worry"],
    "severity": "moderate",
    "risk_level": "low"
  },
  "context_used": true,
  "num_examples_retrieved": 5
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have been feeling anxious",
    "use_rag": true
  }'
```

**JavaScript Example:**
```javascript
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "I've been feeling anxious",
    use_rag: true
  })
});
const data = await response.json();
console.log(data.response);
```

---

### 3. Sentiment Analysis Endpoint

**POST** `/api/analyze-sentiment`

Analyze emotional content and sentiment of text.

**Request Body:**
```json
{
  "text": "I feel hopeless and can't see a way forward"
}
```

**Parameters:**
- `text` (string, required) - Text to analyze

**Response:**
```json
{
  "sentiment": "negative",
  "confidence": 0.92,
  "primary_emotions": ["sadness", "hopelessness", "despair"],
  "severity": "severe",
  "risk_level": "high",
  "explanation": "The text indicates significant emotional distress...",
  "risk_indicators": ["hopeless", "can't see a way"],
  "suggested_response_tone": "compassionate and urgent"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I feel hopeless and cant sleep"
  }'
```

---

### 4. Diagnosis Insights Endpoint

**POST** `/api/diagnose`

Get educational insights about symptoms (NOT medical diagnosis).

**Request Body:**
```json
{
  "symptoms": ["insomnia", "fatigue", "loss of appetite", "sadness"],
  "duration": "2 weeks",
  "additional_info": "Started after a stressful event"
}
```

**Parameters:**
- `symptoms` (array of strings, required) - List of symptoms
- `duration` (string, required) - How long symptoms have persisted
- `additional_info` (string, optional) - Additional context

**Response:**
```json
{
  "insights": "Based on the symptom pattern you've described...",
  "similar_cases_found": 3,
  "symptoms_analyzed": ["insomnia", "fatigue", "loss of appetite", "sadness"],
  "duration": "2 weeks"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/diagnose" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["insomnia", "fatigue", "sadness"],
    "duration": "2 weeks"
  }'
```

---

### 5. Health Check Endpoint

**GET** `/api/health`

Check system health and availability.

**Response:**
```json
{
  "status": "healthy",
  "claude_available": true,
  "datasets_loaded": {
    "counseling": true,
    "sentiment": true,
    "diagnosis": false
  },
  "active_sessions": 5
}
```

**Status Values:**
- `healthy` - All systems operational
- `degraded` - Some issues but functional
- `unhealthy` - Major issues

**cURL Example:**
```bash
curl http://localhost:8000/api/health
```

---

### 6. Dataset Statistics Endpoint

**GET** `/api/stats`

Get statistics about loaded datasets.

**Response:**
```json
{
  "counseling_data": {
    "total_conversations": 3500,
    "avg_context_length": 245.3,
    "avg_response_length": 512.7
  },
  "sentiment_data": {
    "total_records": 8,
    "sentiment_distribution": {
      "negative": 5,
      "positive": 3
    },
    "available_columns": ["text", "sentiment", "emotion"]
  },
  "diagnosis_data": {
    "total_records": 8,
    "conditions": {
      "Depression": 2,
      "Anxiety Disorder": 2,
      "PTSD": 1,
      "OCD": 1,
      "Bipolar Disorder": 1,
      "Generalized Anxiety": 1
    },
    "available_columns": ["symptoms", "duration", "condition", "treatment_approach", "severity"]
  }
}
```

**cURL Example:**
```bash
curl http://localhost:8000/api/stats
```

---

### 7. Get Session History

**GET** `/api/session/{session_id}`

Retrieve conversation history for a session.

**Path Parameters:**
- `session_id` (string, required) - Session ID

**Response:**
```json
{
  "session_id": "abc-123-def",
  "message_count": 6,
  "history": [
    {
      "role": "user",
      "content": "I'm feeling anxious"
    },
    {
      "role": "assistant",
      "content": "I hear that you're experiencing anxiety..."
    }
  ]
}
```

**cURL Example:**
```bash
curl http://localhost:8000/api/session/your-session-id
```

---

### 8. Clear Session

**DELETE** `/api/session/{session_id}`

Clear conversation history for a session.

**Path Parameters:**
- `session_id` (string, required) - Session ID to clear

**Response:**
```json
{
  "message": "Session abc-123-def cleared successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/session/your-session-id
```

---

## Error Responses

All endpoints may return error responses in this format:

**400 Bad Request**
```json
{
  "detail": "Invalid request parameters"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error message"
}
```

---

## Rate Limiting

Currently no rate limiting (hackathon version). In production, consider:
- 100 requests per minute per IP
- 1000 requests per hour per user

---

## CORS

Configure allowed origins in `.env`:
```
ALLOWED_ORIGINS=http://localhost:3000,http://your-frontend-url
```

---

## Interactive Documentation

Visit these URLs when the server is running:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Both provide interactive API testing interfaces.

---

## Response Times

Expected response times:
- `/api/health` - <100ms
- `/api/stats` - <100ms
- `/api/analyze-sentiment` - 2-4 seconds (Claude API)
- `/api/chat` - 2-5 seconds (Claude API + RAG)
- `/api/diagnose` - 2-5 seconds (Claude API)

---

## Best Practices

### 1. Session Management
```javascript
// Store session ID for multi-turn conversations
let sessionId = null;

async function chat(message) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      message,
      session_id: sessionId
    })
  });
  const data = await response.json();
  sessionId = data.session_id; // Save for next message
  return data;
}
```

### 2. Error Handling
```javascript
try {
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message: userInput })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  
  const data = await response.json();
  // Handle response
} catch (error) {
  console.error('API Error:', error);
  // Show user-friendly error message
}
```

### 3. Crisis Detection
```javascript
const data = await fetch('/api/analyze-sentiment', {
  method: 'POST',
  body: JSON.stringify({ text: userMessage })
}).then(r => r.json());

if (data.risk_level === 'critical' || data.risk_level === 'high') {
  // Show crisis resources
  showCrisisResources();
}
```

---

## Webhook Integration (Future)

Future versions may support webhooks for:
- Session expiry notifications
- Crisis alert notifications
- Daily usage reports

---

## SDK Support (Future)

Planned SDKs:
- JavaScript/TypeScript
- Python
- React Hooks
- Vue Composables

---

## Support

For issues or questions:
- Check the logs: `logs/mindpulse.log`
- Review documentation: `README.md`
- Test with: `python test_api.py`

---

**Last Updated:** October 2025  
**API Version:** 1.0.0

