# MindPulse Setup Guide

This guide will walk you through setting up the MindPulse system step by step.

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Anthropic API key (get one at https://console.anthropic.com/)
- Kaggle account for dataset downloads

## 🚀 Quick Start

### 1. Navigate to Project Directory

```bash
cd /Users/wasifsmacbookpro/Desktop/Oct-4-Hackathon-2025-/submissions/MindPulse
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all necessary packages including:
- FastAPI and Uvicorn (web framework)
- Anthropic Claude SDK
- Sentence Transformers (for embeddings)
- Pandas (data processing)
- And more...

### 4. Download Datasets

#### Dataset 1: Mental Health Counseling Conversations ✅
**Already downloaded!** Located at `dataset/mentalHealthCounselingConversations/`

#### Dataset 2: Sentiment Analysis for Mental Health

1. Go to https://www.kaggle.com/datasets/suchintikasarkar/sentiment-analysis-for-mental-health
2. Click "Download" button
3. Extract the downloaded files
4. Create directory: `mkdir -p dataset/sentiment_analysis`
5. Move the CSV files to `dataset/sentiment_analysis/`

```bash
mkdir -p dataset/sentiment_analysis
# After downloading from Kaggle:
# mv ~/Downloads/sentiment_analysis_files/* dataset/sentiment_analysis/
```

#### Dataset 3: Mental Health Diagnosis and Treatment Monitoring

1. Go to https://www.kaggle.com/datasets/uom190346a/mental-health-diagnosis-and-treatment-monitoring
2. Click "Download" button
3. Extract the downloaded files
4. Create directory: `mkdir -p dataset/diagnosis_treatment`
5. Move the CSV files to `dataset/diagnosis_treatment/`

```bash
mkdir -p dataset/diagnosis_treatment
# After downloading from Kaggle:
# mv ~/Downloads/diagnosis_treatment_files/* dataset/diagnosis_treatment/
```

**Note:** If you don't download datasets 2 and 3, the system will create placeholder data for demo purposes.

### 5. Configure Environment Variables

```bash
# Copy the template
cp env-template.txt .env

# Edit the .env file
nano .env
# or use your favorite text editor
```

**Required Configuration:**

```env
# Get your API key from https://console.anthropic.com/
ANTHROPIC_API_KEY=your_actual_api_key_here

# Optional: Customize these if needed
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
CLAUDE_MODEL=claude-3-5-sonnet-20241022
MAX_CONTEXT_EXAMPLES=5
```

### 6. Create Logs Directory

```bash
mkdir -p logs
```

### 7. Test Configuration

```bash
python config.py
```

You should see:
```
✅ Configuration validated successfully!
📊 Dataset directory: /path/to/dataset
🤖 Claude model: claude-3-5-sonnet-20241022
🌐 API host: 0.0.0.0:8000
```

### 8. Start the Server

```bash
python main.py
```

You should see:
```
============================================================
🧠 MindPulse - AI-Powered Mental Health Support System
============================================================
🚀 Starting MindPulse API Server
📍 Host: 0.0.0.0
🔌 Port: 8000
🤖 Claude Model: claude-3-5-sonnet-20241022
📊 Max Context Examples: 5

📖 API Documentation: http://localhost:8000/docs
📘 ReDoc: http://localhost:8000/redoc
============================================================
```

### 9. Test the API

Open a new terminal window and run:

```bash
python test_api.py
```

Or open your browser and go to:
- **Interactive API docs:** http://localhost:8000/docs
- **Alternative docs:** http://localhost:8000/redoc

## 🧪 Testing with cURL

### Chat Endpoint
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have been feeling really anxious lately",
    "use_rag": true
  }'
```

### Sentiment Analysis
```bash
curl -X POST "http://localhost:8000/api/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I feel hopeless and cant sleep"
  }'
```

### Diagnosis Insights
```bash
curl -X POST "http://localhost:8000/api/diagnose" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["insomnia", "fatigue", "sadness"],
    "duration": "2 weeks"
  }'
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

## 🔧 Troubleshooting

### Issue: "ANTHROPIC_API_KEY is not set"
**Solution:** Make sure you created a `.env` file and added your API key.

### Issue: "Module not found"
**Solution:** Make sure you installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution:** Either:
1. Kill the process using port 8000:
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```
2. Or change the port in `.env`:
   ```env
   FASTAPI_PORT=8001
   ```

### Issue: Embeddings model takes too long to download
**Solution:** The first time you run the server, it downloads the sentence transformer model. This is a one-time download. Alternatively, you can use a smaller model in `.env`:
```env
EMBEDDING_MODEL=sentence-transformers/paraphrase-MiniLM-L3-v2
```

### Issue: "Dataset not found" warnings
**Solution:** The system will work with placeholder data for missing datasets. To use real data, download from Kaggle and place in the correct directories (see step 4).

## 🌐 Connecting to Your Web Application

To connect your web application to the MindPulse API:

1. **Add your frontend URL to CORS settings** in `.env`:
   ```env
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://your-frontend-url
   ```

2. **Use the API endpoints** in your frontend:
   ```javascript
   // Example: Chat with the AI
   const response = await fetch('http://localhost:8000/api/chat', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
     },
     body: JSON.stringify({
       message: userMessage,
       session_id: sessionId,
       use_rag: true
     })
   });
   
   const data = await response.json();
   console.log(data.response);
   ```

## 📚 Next Steps

1. **Explore the API Documentation:** http://localhost:8000/docs
2. **Review the code:** Check out the different modules in the project
3. **Customize prompts:** Edit files in `prompts/` directory
4. **Add features:** Extend the API with new endpoints
5. **Deploy:** Consider deploying to a cloud platform for the hackathon demo

## 🎓 Understanding the Architecture

- **`main.py`** - Entry point, starts the server
- **`config.py`** - Configuration management
- **`api/routes.py`** - FastAPI endpoints
- **`agents/claude_agent.py`** - Claude AI integration
- **`data_loaders/`** - Dataset loading and processing
- **`prompts/`** - Prompt engineering templates
- **`utils/`** - Helper functions

## 💡 Tips for the Hackathon

1. **Start with the interactive docs** - They make it easy to test endpoints
2. **Monitor the logs** - The console output shows what's happening
3. **Use session IDs** - For multi-turn conversations
4. **Experiment with prompts** - Customize in `prompts/` directory
5. **Check dataset stats** - Use `/api/stats` to understand your data

## ⚠️ Important Reminders

- This is for educational/hackathon purposes only
- Not a replacement for professional mental health services
- Always include crisis resources in user-facing applications
- Be mindful of data privacy and security

## 🆘 Need Help?

- Check the logs in `logs/mindpulse.log`
- Review error messages in the console
- Consult the README.md for more information
- Ask your hackathon mentors or teammates

Good luck with your hackathon! 🚀

