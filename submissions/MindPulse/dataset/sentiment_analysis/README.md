# Sentiment Analysis Dataset

## 📥 Download Instructions

1. Go to: https://www.kaggle.com/datasets/suchintikasarkar/sentiment-analysis-for-mental-health
2. Click the "Download" button
3. Extract the downloaded files
4. Place all CSV files in this directory

## 📁 Expected Files

After downloading, this directory should contain CSV files with sentiment-labeled mental health text data.

## ⚠️ Note

If you don't download this dataset, MindPulse will automatically use placeholder data for demonstration purposes. The system will work fine, but having real data improves the quality of sentiment analysis.

## 🔧 File Format

The dataset typically includes:
- `text` - Mental health related text/statements
- `sentiment` or `label` - Sentiment classification (positive/negative/neutral)
- `emotion` - Specific emotion labels (optional)

## ✅ Verification

After placing files here, restart the MindPulse server. Check the logs to confirm:
```
✅ Loaded N sentiment records
```

If you see:
```
⚠️ No CSV files found in sentiment data directory
```

Then the system is using placeholder data (which is fine for hackathon purposes!).

