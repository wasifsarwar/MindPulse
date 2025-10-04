# Mental Health Diagnosis and Treatment Dataset

## 📥 Download Instructions

1. Go to: https://www.kaggle.com/datasets/uom190346a/mental-health-diagnosis-and-treatment-monitoring
2. Click the "Download" button
3. Extract the downloaded files
4. Place all CSV files in this directory

## 📁 Expected Files

After downloading, this directory should contain CSV files with mental health diagnosis and treatment data.

## ⚠️ Note

If you don't download this dataset, MindPulse will automatically use placeholder data for demonstration purposes. The system will work fine, but having real data improves the quality of diagnosis insights.

## 🔧 File Format

The dataset typically includes:
- `symptoms` - List of reported symptoms
- `diagnosis` or `condition` - Mental health condition
- `treatment` or `treatment_approach` - Treatment methods
- `duration` - How long symptoms persisted
- `severity` - Severity level (optional)

## ✅ Verification

After placing files here, restart the MindPulse server. Check the logs to confirm:
```
✅ Loaded N diagnosis records
```

If you see:
```
⚠️ No CSV files found in diagnosis data directory
```

Then the system is using placeholder data (which is fine for hackathon purposes!).

## 🎯 Usage

This data is used to:
- Find similar cases based on symptoms
- Provide educational information about conditions
- Suggest treatment approaches (educational, not prescriptive)
- Help users understand patterns in their symptoms

