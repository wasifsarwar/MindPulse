# SMS Alert Setup (Twilio)

MindPulse can automatically alert healthcare providers when mental health deterioration is detected.

## 🚨 When Alerts Are Sent

The system sends SMS alerts to providers when it detects:

**Criteria:**
- Mood rating ≤ 3 (very low) 
- Sleep quality ≤ 3 (very poor)
- Medication not taken
- Physical activity ≤ 2 (minimal)

**Alert triggers:**
- 3 or more concerning factors, OR
- High risk level with 2+ factors, OR
- Critical mood + no medication

## 📱 Setup Instructions

### 1. Get Twilio Account (Free Trial)

1. Sign up at https://www.twilio.com/try-twilio
2. Verify your phone number
3. Get free trial credits ($15 USD)

### 2. Get Credentials

From your Twilio Console:

1. **Account SID**: Found on dashboard
2. **Auth Token**: Click "Show" to reveal
3. **Phone Number**: Get a free trial number

### 3. Configure `.env`

Edit `server/.env`:

```env
# SMS Notifications
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15551234567
PROVIDER_PHONE_NUMBER=+15559876543
ENABLE_SMS_ALERTS=True
```

**Important:**
- Use format `+1` for US numbers (include country code)
- `TWILIO_PHONE_NUMBER` = Your Twilio number
- `PROVIDER_PHONE_NUMBER` = Healthcare provider's number

### 4. Install Twilio

```bash
cd server
pip install twilio
```

### 5. Test It

```bash
python3 main.py
```

Then submit a survey with concerning responses:
- Medication: No
- Mood: 2/10
- Sleep: 2/10
- Activity: 1/10
- Thoughts: "Feeling hopeless"

The provider should receive an SMS like:

```
🚨 MindPulse Alert - HIGH Risk

Patient check-in shows concerning patterns:
• Risk Level: high
• Concerns: low_mood, poor_sleep, missed_medication
• Time: Just now

Please review patient status.
- MindPulse System
```

## 🔧 Development Mode

To develop without sending real SMS:

```env
ENABLE_SMS_ALERTS=False
```

The system will:
- Still detect deterioration
- Log alerts to console
- NOT send actual SMS
- Return `provider_contacted: false`

## 💰 Costs

**Twilio Free Trial:**
- $15 free credits
- ~$0.0075 per SMS
- ~2000 free messages

**After trial:**
- Pay as you go
- No monthly fee
- Only pay for messages sent

## 🧪 Testing Without Real Numbers

**Twilio Trial Restrictions:**
- Can only send to verified numbers
- Add test numbers in Twilio Console → Phone Numbers → Verified Caller IDs

**For Demo:**
1. Verify your own phone number
2. Set it as `PROVIDER_PHONE_NUMBER`
3. Test alerts come to your phone

## 🔒 Security

**Best Practices:**
- Never commit `.env` file to git
- Keep auth token secret
- Use environment variables in production
- Consider Twilio subaccounts for different environments

## ⚠️ Important Notes

1. **HIPAA Compliance**: Standard Twilio SMS is NOT HIPAA-compliant
   - For production, use Twilio's HIPAA-compliant service
   - Don't send PHI via SMS without proper BAA

2. **Testing**: Always test with demo/test data first

3. **False Positives**: The detection algorithm may trigger on legitimate low scores
   - Adjust thresholds in `utils/sms.py` if needed

4. **Provider Phone**: Ensure provider consents to receiving alerts

## 🎯 Customizing Alert Logic

Edit `server/utils/sms.py`:

```python
def is_deterioration_detected(...):
    # Modify these thresholds:
    critical_mood = mood_rating <= 3  # Change to 2 for stricter
    critical_sleep = sleep_quality <= 3
    # ... etc
```

## 📊 Monitoring

Check logs for alert activity:

```bash
tail -f logs/mindpulse.log | grep "deterioration\|alert"
```

You'll see:
- ⚠️ When deterioration is detected
- ✅ When SMS sent successfully
- ❌ If SMS fails

## 🆘 Troubleshooting

**SMS not sending?**

1. Check `.env` configuration
2. Verify `ENABLE_SMS_ALERTS=True`
3. Check Twilio credentials
4. Ensure phone numbers include country code
5. Check Twilio trial number can send to destination
6. Review logs: `logs/mindpulse.log`

**"SMS configuration incomplete"?**
- All 4 Twilio settings must be filled in `.env`

**"Invalid phone number"?**
- Use E.164 format: `+1234567890` (with `+` and country code)

## 📖 Alternative: Email Alerts

To use email instead of SMS, modify `utils/sms.py`:

```python
import smtplib
from email.mime.text import MIMEText

def send_provider_alert(...):
    # Use SMTP to send email
    # ... implementation
```

---

**For Hackathon Demo:**
Set `ENABLE_SMS_ALERTS=False` to avoid charges, or use your own phone as the provider number for testing!
