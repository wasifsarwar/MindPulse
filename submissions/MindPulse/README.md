# MindPulse - AI Mental Health Support System

AI-powered mental health support using Claude with RAG (Retrieval-Augmented Generation).

## 🚀 Quick Start

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd server
   pip install -r requirements.txt
   ```

   *(Optional)* **For SMS alerts**: See [SMS_SETUP.md](server/SMS_SETUP.md)

2. **Configure API Key**
```bash
cd server
cp env-template.txt .env
# Edit .env and add your Anthropic API key
nano .env
```

Get your API key: https://console.anthropic.com/

3. **Start Backend Server**
```bash
cd server
python3 main.py
```

Server runs on: http://localhost:8000

### Web App Setup

4. **Install Frontend Dependencies**
```bash
cd web
npm install
```

5. **Start Web App**
```bash
npm start
```

App opens at: http://localhost:3000

### Test the Complete System

Open http://localhost:3000 in your browser, fill out the survey, and see Claude's empathetic response!

## 📁 Project Structure

```
MindPulse/
├── README.md
├── dataset/                    # Kaggle datasets
│   ├── mentalHealthCounselingConversations/
│   ├── sentiment_analysis/
│   └── diagnosis_treatment/
├── server/                     # Backend (Python)
│   ├── main.py                 # Entry point
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Dependencies
│   ├── .env                   # API keys (create this)
│   ├── agents/                # Claude AI agent
│   ├── api/                   # FastAPI routes
│   ├── data_loaders/          # Dataset loaders
│   ├── prompts/               # Prompt engineering
│   └── utils/                 # Utilities
└── web/                       # Frontend (TypeScript React)
    ├── public/
    ├── src/
    │   ├── components/        # Survey form & results
    │   ├── services/          # API calls
    │   ├── types/             # TypeScript types
    │   └── App.tsx            # Main component
    ├── package.json
    └── README.md
```

## 🎯 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/analyze-survey` | POST | **Daily survey analysis** (for your web app) |
| `/api/chat` | POST | Mental health chat |
| `/api/analyze-sentiment` | POST | Sentiment analysis |
| `/api/diagnose` | POST | Symptom insights |
| `/api/health` | GET | System status |
| `/api/stats` | GET | Dataset statistics |

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

**🚨 Provider Alert Feature:**
- If mental health deterioration is detected (e.g., very low mood, missed medication)
- `provider_contacted` will be `true`
- An SMS is automatically sent to the configured healthcare provider
- Web UI displays a notification to the user

## 📖 API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## 🧪 Testing

**Test the survey endpoint:**
```bash
cd server
python3 test_survey.py
```

**Test all endpoints:**
```bash
cd server
python3 test_api.py
```

**Manual test (cURL):**
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

**Interactive docs:**
Open browser: http://localhost:8000/docs

## 📊 Datasets

Three Kaggle datasets:
1. **Counseling Conversations** (3,512 conversations) ✅ Included
2. **Sentiment Analysis** - Download from Kaggle
3. **Diagnosis & Treatment** - Download from Kaggle

The system works with placeholder data if datasets 2 & 3 aren't downloaded.

## 🛠️ Tech Stack

- **Backend:** FastAPI + Python
- **AI:** Claude 3.5 Sonnet (Anthropic)
- **RAG:** Sentence Transformers
- **SMS:** Twilio (optional)
- **Data:** Pandas + NumPy
- **Frontend:** TypeScript + React

## 🔧 Configuration

Edit `server/.env`:
```env
ANTHROPIC_API_KEY=your_key_here
FASTAPI_PORT=8000
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# SMS Alerts (Optional - for provider notifications)
ENABLE_SMS_ALERTS=False
TWILIO_ACCOUNT_SID=your_twilio_sid


## ⚠️ Important

This is for educational/hackathon purposes only. NOT a replacement for professional mental health care.

**Crisis Resources:**
- Suicide Prevention Lifeline: 988 or 1-800-273-8255
- Crisis Text Line: Text HOME to 741741

## 📝 License

For hackathon use.
