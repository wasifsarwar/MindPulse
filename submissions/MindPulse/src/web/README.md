# MindPulse Web App

Beautiful, empathetic TypeScript React interface for MindPulse mental health check-ins.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd web
npm install
```

### 2. Make Sure Backend is Running

The web app connects to the FastAPI backend on `http://localhost:8000`.

```bash
# In another terminal
cd ../server
python3 main.py
```

### 3. Start the Web App

```bash
npm start
```

The app will open at `http://localhost:3000`

## ✨ Features

- **5 Survey Questions:**
  1. Medication adherence (checkbox)
  2. Mood rating (1-10 slider)
  3. Sleep quality (1-10 slider)
  4. Physical activity (1-10 slider)
  5. Thoughts (textarea)

- **Claude AI Response:**
  - Empathetic personal message
  - 2-3 actionable recommendations
  - Risk level assessment
  - Key concerns identified

- **Beautiful UI:**
  - Modern gradient design
  - Smooth animations
  - Responsive (mobile-friendly)
  - Accessible forms

## 📁 Project Structure

```
web/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── SurveyForm.tsx      # 5-question survey
│   │   └── ResultDisplay.tsx   # Claude's response
│   ├── services/
│   │   └── api.ts              # API calls
│   ├── types/
│   │   └── index.ts            # TypeScript types
│   ├── App.tsx                 # Main component
│   ├── App.css                 # Styling
│   ├── index.tsx               # Entry point
│   └── index.css
├── package.json
└── tsconfig.json
```

## 🎨 Customization

### Change Colors

Edit `App.css`:
- Primary gradient: `.app` background
- Accent color: `#667eea` throughout

### Modify Questions

Edit `SurveyForm.tsx` to add/change questions.

### API Endpoint

Change in `src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://your-api-url';
```

## 🧪 Testing

1. Fill out all 5 questions
2. Click "Submit Check-In"
3. View Claude's empathetic response

## 📱 Mobile Responsive

The app works beautifully on:
- Desktop (600px width, centered)
- Tablet (adapts to screen)
- Mobile (stacked layout)

## 🔧 Tech Stack

- React 18
- TypeScript 5
- Create React App
- CSS3 (no framework)
- Inter font (Google Fonts)

## ⚠️ Important

This is for educational/hackathon purposes. Not a replacement for professional mental health care.

**Crisis Resources:**
- 988: Suicide Prevention Lifeline
- Text HOME to 741741: Crisis Text Line

