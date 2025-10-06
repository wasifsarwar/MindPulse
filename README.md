# MindPulse - AI Mental Health Support System

AI-powered mental health support using Claude with RAG (Retrieval-Augmented Generation).

## 🎥 Product Demo

See MindPulse in action across three real-world scenarios:

### Scenario 1: High Wellbeing ✅
**When things are going well**

https://github.com/user-attachments/assets/YOUR_VIDEO_ID_HERE_1

*User reports positive mood, good sleep, and consistent medication adherence. MindPulse provides positive reinforcement and encouragement to maintain healthy habits.*

**To embed this video:** Upload `videos/MindPulseGreat.mp4` to a GitHub issue comment, then copy the generated URL and replace the placeholder above.

---

### Scenario 2: Moderate Concerns ⚠️
**When you're feeling "just okay"**

https://github.com/user-attachments/assets/YOUR_VIDEO_ID_HERE_2

*User reports mediocre mood despite good physical health. MindPulse detects the discrepancy and provides balanced, realistic support with actionable recommendations.*

**To embed this video:** Upload `videos/MindPulseMeh.mp4` to a GitHub issue comment, then copy the generated URL and replace the placeholder above.

---

### Scenario 3: High Risk 🚨
**When immediate support is needed**

https://github.com/user-attachments/assets/YOUR_VIDEO_ID_HERE_3

*User reports concerning patterns (low mood, missed medication, poor sleep). MindPulse escalates appropriately, provides crisis resources, and automatically alerts the healthcare provider.*

**To embed this video:** Upload `videos/MindPulseWorse.mp4` to a GitHub issue comment, then copy the generated URL and replace the placeholder above.

---

> **💡 How to embed videos in GitHub README:**
> 1. Create a new issue in your repo (you can delete it later)
> 2. Drag and drop each video file into the issue comment box
> 3. Wait for it to upload and generate a URL like `https://github.com/user-attachments/assets/...`
> 4. Copy that URL and paste it directly into the README (replace the placeholders above)
> 5. The video will then play inline in your README!

---

## 🚀 Quick Start

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd src/server
   pip install -r requirements.txt
   ```

   *(Optional)* **For SMS alerts**: See [src/server/SMS_SETUP.md](src/server/SMS_SETUP.md)

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

## 🎬 Video Scenarios

All demo videos are located in the [`videos/`](./videos/) folder:
- [`MindPulseGreat.mp4`](./videos/MindPulseGreat.mp4) - High wellbeing scenario
- [`MindPulseMeh.mp4`](./videos/MindPulseMeh.mp4) - Moderate concerns scenario  
- [`MindPulseWorse.mp4`](./videos/MindPulseWorse.mp4) - High risk scenario

> **Note:** Click the badges in the Product Demo section above to view/download each scenario video.

## 📁 Project Structure

```
MindPulse/
├── README.md
├── videos/                        # Product demo videos
│   ├── MindPulseGreat.mp4
│   ├── MindPulseMeh.mp4
│   └── MindPulseWorse.mp4
├── src/
│   ├── dataset/                    # Kaggle datasets
│   │   ├── mentalHealthCounselingConversations/
│   │   ├── sentiment_analysis/
│   │   └── diagnosis_treatment/
│   ├── server/                     # Backend (Python)
│   │   ├── main.py                 # Entry point
│   │   ├── config.py              # Configuration
│   │   ├── requirements.txt       # Dependencies
│   │   ├── .env                   # API keys (create this)
│   │   ├── agents/                # Claude AI agent
│   │   ├── api/                   # FastAPI routes
│   │   ├── data_loaders/          # Dataset loaders
│   │   ├── prompts/               # Prompt engineering
│   │   ├── utils/                 # Utilities
│   │   └── tests/                 # Test files
│   └── web/                       # Frontend (TypeScript React)
│       ├── public/
│       ├── src/
│       │   ├── components/        # Survey form & results
│       │   ├── services/          # API calls
│       │   ├── types/             # TypeScript types
│       │   └── App.tsx            # Main component
│       ├── package.json
│       └── README.md
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
cd src/server/tests
python3 test_survey.py
```

**Test all endpoints:**
```bash
cd src/server/tests
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
