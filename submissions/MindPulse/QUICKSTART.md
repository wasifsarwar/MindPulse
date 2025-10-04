# MindPulse - Quick Start Guide

Get MindPulse running in 5 minutes!

## 🚀 Super Fast Setup

### 1. Install Dependencies (1 min)

```bash
cd /Users/wasifsmacbookpro/Desktop/Oct-4-Hackathon-2025-/submissions/MindPulse
pip install -r requirements.txt
```

### 2. Set Your API Key (30 seconds)

```bash
# Copy the template
cp env-template.txt .env

# Edit and add your Anthropic API key
echo 'ANTHROPIC_API_KEY=your_key_here' >> .env
```

Get your API key: https://console.anthropic.com/

### 3. Start the Server (10 seconds)

```bash
python main.py
```

### 4. Test It! (30 seconds)

**Option A: Web Browser**
- Open: http://localhost:8000/docs
- Try the `/api/chat` endpoint
- Click "Try it out"
- Send a message!

**Option B: Test Script**
```bash
# In a new terminal
python test_api.py
```

**Option C: Frontend Demo**
- Open `frontend_example.html` in your browser
- Start chatting!

## 📱 Try These Examples

### Chat
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I have been feeling anxious"}'
```

### Sentiment Analysis
```bash
curl -X POST "http://localhost:8000/api/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel hopeless"}'
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

## 🎨 Connect Your Web App

```javascript
// Simple fetch example
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userInput,
    use_rag: true
  })
});

const data = await response.json();
console.log(data.response);
```

## 📊 What's Included

✅ **Dataset 1:** Mental Health Counseling Conversations (Already loaded!)
⏳ **Dataset 2:** Sentiment Analysis (Optional - will use placeholder)
⏳ **Dataset 3:** Diagnosis & Treatment (Optional - will use placeholder)

The system works perfectly with just Dataset 1! The other datasets enhance it but aren't required.

## 🎯 Key Features

- 💬 **Chat:** Mental health support conversations
- 🎭 **Sentiment:** Real-time emotion analysis
- 🏥 **Insights:** Educational health information
- 📝 **Sessions:** Maintains conversation context
- 🔍 **RAG:** Retrieves relevant counseling examples

## 🛠️ Troubleshooting

**Problem:** "ANTHROPIC_API_KEY is not set"
**Solution:** Create `.env` file with your API key

**Problem:** "Port 8000 in use"
**Solution:** Change port in `.env`: `FASTAPI_PORT=8001`

**Problem:** Can't connect from web app
**Solution:** Add your frontend URL to `.env`:
```
ALLOWED_ORIGINS=http://localhost:3000,http://your-url
```

## 📚 Next Steps

1. **Read ARCHITECTURE.md** - Understand how it works
2. **Read SETUP_GUIDE.md** - Detailed setup instructions
3. **Customize prompts** - Edit files in `prompts/` folder
4. **Add features** - Extend the API
5. **Deploy** - Take it to production!

## 🎓 Hackathon Tips

- ✨ The interactive docs (`/docs`) are your best friend
- 🔄 Use session IDs for multi-turn conversations
- 📊 Check `/api/stats` to see your data
- 🎨 Customize prompts in `prompts/` directory
- 🔧 Monitor logs in console for debugging

## ⚠️ Important

This is for **educational/hackathon purposes** only.
NOT a replacement for professional mental health services.

## 💡 API Endpoints Cheat Sheet

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/chat` | POST | Main conversation |
| `/api/analyze-sentiment` | POST | Sentiment analysis |
| `/api/diagnose` | POST | Symptom insights |
| `/api/health` | GET | System status |
| `/api/stats` | GET | Dataset statistics |
| `/api/session/{id}` | GET | Get history |
| `/api/session/{id}` | DELETE | Clear session |

## 🆘 Need Help?

- Check `logs/mindpulse.log` for errors
- Review console output
- Try the test script: `python test_api.py`
- Check your `.env` configuration

---

**Ready to build something amazing! 🚀**

For detailed information, see:
- `README.md` - Complete documentation
- `SETUP_GUIDE.md` - Step-by-step setup
- `ARCHITECTURE.md` - System design deep dive

