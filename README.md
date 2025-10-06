# MindPulse - AI Mental Health Support System

AI-powered mental health support using Claude with RAG (Retrieval-Augmented Generation).

## Product Demo

MindPulse adapts its responses based on mental health risk levels:

### Scenario 1: Low Risk - High Wellbeing

https://github.com/user-attachments/assets/afbf4a3b-fc41-488a-8e57-bfedeb2ed19d

User reports positive mood, good sleep, and consistent medication. MindPulse provides positive reinforcement and encouragement.

---

### Scenario 2: Moderate Risk - Discrepancy Detected

https://github.com/user-attachments/assets/a6fd6793-fdfa-4bb6-967f-e0bfd963210f

User reports mediocre mood despite good physical health. MindPulse detects this discrepancy and provides balanced support with actionable recommendations.

---

### Scenario 3: High Risk - Intervention Required

https://github.com/user-attachments/assets/4cc5b36f-a711-435a-add2-f3f29c561aa9

User reports concerning patterns (low mood, missed medication, poor sleep). MindPulse escalates appropriately with crisis resources and automatically alerts the healthcare provider.

---

## Quick Start

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd src/server
   pip install -r requirements.txt
   ```

   Optional: For SMS alerts, see [src/server/SMS_SETUP.md](src/server/SMS_SETUP.md)

2. **Configure API Key**
```bash
cd src/server
cp env-template.txt .env
# Edit .env and add your Anthropic API key
nano .env
```

Get your API key: https://console.anthropic.com/

3. **Start Backend Server**
```bash
cd src/server
python3 main.py
```

Server runs on: http://localhost:8000

### Web App Setup

4. **Install Frontend Dependencies**
```bash
cd src/web
npm install
```

5. **Start Web App**
```bash
npm start
```

App opens at: http://localhost:3000

### Test the Complete System

Open http://localhost:3000 in your browser, fill out the survey, and see Claude's empathetic response!


## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/analyze-survey` | POST | Daily survey analysis (primary endpoint) |
| `/api/chat` | POST | Conversational mental health support |
| `/api/analyze-sentiment` | POST | Sentiment and emotion analysis |
| `/api/diagnose` | POST | Symptom pattern insights |
| `/api/health` | GET | System health check |
| `/api/stats` | GET | Dataset statistics |
| `/api/session/{id}` | GET | Get conversation history |
| `/api/session/{id}` | DELETE | Clear conversation history |

### Survey Endpoint (Main endpoint for your web app)

**POST** `/api/analyze-survey`

Send your 5 survey questions in one request:

```json
{
  "medication_taken": false,
  "mood_rating": 4,
  "sleep_quality": 3,
  "physical_activity": 2,
  "thoughts": "I've been feeling overwhelmed..."
}
```

Response:
```json
{
  "message": "I hear that you're feeling overwhelmed...",
  "recommendations": [
    "Try setting a reminder for your medication",
    "Even 10 minutes of gentle movement can help",
    "Consider reaching out to someone you trust"
  ],
  "risk_level": "moderate",
  "key_concerns": ["low_mood", "poor_sleep", "missed_medication"],
  "provider_contacted": false
}
```

**Provider Alert Feature:**
- If mental health deterioration is detected (e.g., very low mood, missed medication)
- `provider_contacted` will be `true`
- An SMS is automatically sent to the configured healthcare provider
- Web UI displays a notification to the user

**Interactive API Documentation:** http://localhost:8000/docs (Swagger) or http://localhost:8000/redoc

## Key Features

- **Risk-Based Assessment**: Automatically classifies responses as low, moderate, or high risk
- **Discrepancy Detection**: Identifies when physical health metrics don't match emotional state
- **Contextual Responses**: Uses RAG with 3,512+ counseling conversations for empathetic replies
- **Provider Alerts**: Automatic SMS notifications to healthcare providers when deterioration is detected
- **Personalized Recommendations**: Tailored, actionable suggestions based on specific concerns
- **Session Management**: Maintains conversation context across interactions
- **Comprehensive Logging**: All interactions logged to `src/logs/mindpulse.log`

## Testing

**Run survey endpoint tests:**
```bash
cd src/server/tests
python3 test_survey.py
```

**Test different scenarios:**
```bash
cd src/server/tests
python3 test_all_scenarios.py      # Test multiple use cases
python3 test_critical_survey.py    # Test high-risk scenarios
python3 test_sms_detection.py      # Test SMS alert system
```

**Manual API test (cURL):**
```bash
curl -X POST http://localhost:8000/api/analyze-survey \
  -H "Content-Type: application/json" \
  -d '{
    "medication_taken": true,
    "mood_rating": 7,
    "sleep_quality": 6,
    "physical_activity": 5,
    "thoughts": "Feeling pretty good today"
  }'
```

**Interactive API documentation:**
Visit http://localhost:8000/docs (Swagger UI) or http://localhost:8000/redoc (ReDoc)

## Datasets

MindPulse uses three mental health datasets for RAG:

1. **Counseling Conversations** - 3,512 mental health counseling conversations
   - Located: `src/dataset/mentalHealthCounselingConversations/`
   - Status: Included in repository

2. **Sentiment Analysis** - Emotional state classification data
   - Located: `src/dataset/sentiment_analysis/`
   - Status: Included in repository

3. **Diagnosis & Treatment** - Symptom patterns and treatment insights
   - Located: `src/dataset/diagnosis_treatment/`
   - Status: Included in repository

All datasets are loaded at startup. The system uses RAG with sentence transformers for semantic search.

## Tech Stack

- **Backend:** FastAPI + Python
- **AI:** Claude 3.5 Sonnet (Anthropic)
- **RAG:** Sentence Transformers
- **SMS:** Twilio (optional)
- **Data:** Pandas + NumPy
- **Frontend:** TypeScript + React

## Configuration

Create `src/server/.env` from the template:

```bash
cd src/server
cp env-template.txt .env
```

Key configuration options:

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# API Settings
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_RELOAD=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# AI Configuration
CLAUDE_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=2048
TEMPERATURE=0.7
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_CONTEXT_EXAMPLES=5

# SMS Alerts (Optional)
ENABLE_SMS_ALERTS=False
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890
PROVIDER_PHONE_NUMBER=+1234567890

# Logging
LOG_LEVEL=INFO
```

See [env-template.txt](src/server/env-template.txt) for all configuration options.

## Important

This is for educational/hackathon purposes only. NOT a replacement for professional mental health care.

**Crisis Resources:**
- Suicide Prevention Lifeline: 988 or 1-800-273-8255
- Crisis Text Line: Text HOME to 741741

## License

For hackathon use.
