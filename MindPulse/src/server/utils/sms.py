"""SMS notification service using Twilio."""

from typing import Optional
from loguru import logger
from config import settings


def send_provider_alert(
    patient_info: str,
    concern_level: str,
    key_concerns: list
) -> bool:
    """
    Send SMS alert to provider about patient deterioration.
    
    Args:
        patient_info: Patient identifier or info
        concern_level: Risk level (moderate/high)
        key_concerns: List of concerning factors
        
    Returns:
        True if SMS sent successfully, False otherwise
    """
    if not settings.enable_sms_alerts:
        logger.info("SMS alerts disabled - skipping provider notification")
        return False
    
    if not all([
        settings.twilio_account_sid,
        settings.twilio_auth_token,
        settings.twilio_phone_number,
        settings.provider_phone_number
    ]):
        logger.warning("SMS configuration incomplete - cannot send alert")
        return False
    
    try:
        from twilio.rest import Client
        
        client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token
        )
        
        # Create alert message
        concerns_text = ", ".join(key_concerns) if key_concerns else "multiple factors"
        
        message_body = f"""
🚨 MindPulse Alert - {concern_level.upper()} Risk

Patient check-in shows concerning patterns:
• Risk Level: {concern_level}
• Concerns: {concerns_text}
• Time: Just now

Please review patient status.
- MindPulse System
        """.strip()
        
        # Send SMS
        message = client.messages.create(
            body=message_body,
            from_=settings.twilio_phone_number,
            to=settings.provider_phone_number
        )
        
        logger.info(f"✅ Provider alert sent successfully (SID: {message.sid})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send provider alert: {e}")
        return False


def is_deterioration_detected(
    medication_taken: bool,
    mood_rating: int,
    sleep_quality: int,
    physical_activity: int,
    risk_level: str
) -> bool:
    """
    Determine if mental health deterioration indicators are present.
    
    Criteria for alerting provider:
    - Medication not taken
    - Mood rating <= 3 (very low)
    - Sleep quality <= 3 (very poor)
    - Physical activity <= 2 (minimal)
    - Risk level is moderate or high
    
    Returns:
        True if deterioration detected and provider should be alerted
    """
    # Check critical indicators
    critical_mood = mood_rating <= 3
    critical_sleep = sleep_quality <= 3
    no_medication = not medication_taken
    minimal_activity = physical_activity <= 2
    elevated_risk = risk_level in ['moderate', 'high']
    
    # Count concerning factors
    concerning_factors = sum([
        critical_mood,
        critical_sleep,
        no_medication,
        minimal_activity
    ])
    
    # Alert if:
    # - 3+ concerning factors, OR
    # - High risk level with 2+ factors, OR
    # - Critical mood + no medication
    should_alert = (
        concerning_factors >= 3 or
        (risk_level == 'high' and concerning_factors >= 2) or
        (critical_mood and no_medication)
    )
    
    if should_alert:
        logger.warning(
            f"⚠️ Deterioration detected: "
            f"factors={concerning_factors}, risk={risk_level}"
        )
    
    return should_alert
