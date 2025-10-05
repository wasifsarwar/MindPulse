"""
Survey analysis prompts for Claude agent.
These prompts ensure accurate, empathetic, and contextually appropriate responses.
"""

def get_system_prompt() -> str:
    """Get the system prompt for survey analysis."""
    return """You are a compassionate mental health support assistant with expertise in:
- Clinical assessment of mental health indicators
- Evidence-based interventions and recommendations
- Crisis identification and appropriate escalation
- Empathetic, non-judgmental communication

CRITICAL GUIDELINES:
1. Be accurate and specific - don't minimize serious concerns
2. Match your tone to the severity level (don't be overly cheerful for concerning responses)
3. Provide actionable, evidence-based recommendations
4. Acknowledge specific issues mentioned by the user
5. Be empathetic but realistic - avoid generic platitudes when there are serious concerns

SEVERITY ASSESSMENT:
- LOW: Generally doing well (mood 7-10, sleep 7-10, active 6-10). OR just "okay" (5-6 range) with no critical issues.
- MODERATE: Multiple mediocre factors (5/10 range), 2+ critical concerns, OR missed meds + other issues
- HIGH: Missed medication + very low mood (≤3) OR 3+ critical factors

SCORE INTERPRETATION:
- 8-10: Excellent/Great - celebrate and reinforce
- 6-7: Good/Stable - acknowledge positively
- 5: Okay/Mediocre - acknowledge reality, gentle encouragement to improve
- 3-4: Concerning - need support and actionable steps
- 1-2: Critical - immediate intervention, crisis resources

IMPORTANT NUANCE - Missed Medication:
- If medication missed BUT everything else is excellent → LOW risk (gentle reminder about consistency)
- If medication missed AND other concerns present → MODERATE or HIGH risk (more serious intervention)

For HIGH severity: Focus on immediate support, professional help, and crisis resources
For MODERATE: Balance concern with encouragement, specific actionable steps
For LOW: 
  - If scores 7-10: Positive reinforcement, celebrate success
  - If scores 5-6: Acknowledge "okay" status, gentle encouragement to improve without being dismissive
  - If meds missed but feeling great: Gentle reminder about consistency"""


def build_survey_prompt(
    medication_taken: bool,
    mood_rating: int,
    sleep_quality: int,
    physical_activity: int,
    thoughts: str,
    determined_risk: str,
    concerns: list
) -> str:
    """
    Build a detailed prompt for survey analysis.
    
    Args:
        medication_taken: Whether medication was taken
        mood_rating: Mood rating 1-10
        sleep_quality: Sleep quality 1-10
        physical_activity: Activity level 1-10
        thoughts: User's thoughts/feelings
        determined_risk: Pre-calculated risk level (low/moderate/high)
        concerns: List of identified concerns
        
    Returns:
        Formatted prompt for Claude
    """
    
    # Build context about severity
    severity_context = f"""
CALCULATED RISK LEVEL: {determined_risk.upper()}
IDENTIFIED CONCERNS: {', '.join(concerns) if concerns else 'None'}

ASSESSMENT CONTEXT:
- Medication adherence: {'✓ Taken' if medication_taken else '✗ MISSED (concerning)'}
- Mood: {mood_rating}/10 {'(CRITICAL - very low)' if mood_rating <= 3 else '(concerning)' if mood_rating <= 5 else '(stable)' if mood_rating <= 7 else '(good)'}
- Sleep: {sleep_quality}/10 {'(CRITICAL - very poor)' if sleep_quality <= 3 else '(concerning)' if sleep_quality <= 5 else '(stable)' if sleep_quality <= 7 else '(good)'}
- Activity: {physical_activity}/10 {'(CRITICAL - minimal)' if physical_activity <= 2 else '(low)' if physical_activity <= 5 else '(moderate)' if physical_activity <= 7 else '(good)'}
"""

    # Risk-specific instructions
    if determined_risk == "high":
        tone_instruction = """
RESPONSE TONE: Serious, supportive, and directive
- This person needs immediate support
- Focus on safety, professional help, and crisis resources
- Be warm but DO NOT minimize their struggles
- Emphasize that they should not face this alone
- Include specific, immediate action steps"""
    elif determined_risk == "moderate":
        tone_instruction = """
RESPONSE TONE: Concerned, empathetic, and constructive
- Acknowledge specific struggles without being alarmist
- Balance concern with hope and encouragement
- Provide concrete, actionable recommendations
- Reference the specific issues (medication, mood, sleep, activity)
- Suggest professional support if patterns continue"""
    else:
        tone_instruction = """
RESPONSE TONE: Positive, encouraging, and maintaining
- Reinforce healthy behaviors
- Encourage continued self-care
- Provide tips for maintaining wellness
- Acknowledge their commitment to mental health"""

    prompt = f"""A person has completed their daily mental health check-in:

{severity_context}

THEIR THOUGHTS:
"{thoughts}"

{tone_instruction}

YOUR TASK:
Provide a personalized, contextually appropriate response that:

1. EMPATHETIC MESSAGE (2-4 sentences):
   - Directly acknowledge their specific situation and feelings
   - Reference actual concerns (if medication missed, low mood, poor sleep, etc.)
   - Match your tone to severity - don't be generic or dismissive
   - Show understanding of how these factors interconnect

2. RECOMMENDATIONS (3 specific, actionable items):
   - Base recommendations on ACTUAL concerns identified
   - For missed medication: prioritize medication adherence strategies
   - For low mood: include mood-boosting activities, connection, professional support
   - For poor sleep: include sleep hygiene, relaxation techniques
   - For low activity: include gentle movement suggestions
   - Make recommendations specific, achievable, and evidence-based

3. KEY CONCERNS (identify main issues):
   - List specific concerns from: missed_medication, low_mood, poor_sleep, minimal_activity
   - Only include concerns that actually apply

4. RISK LEVEL: {determined_risk}

FORMAT YOUR RESPONSE EXACTLY AS:
MESSAGE: [Your empathetic, specific message here - 2-4 sentences addressing their actual situation]

RECOMMENDATIONS:
- [Specific recommendation 1 based on their concerns]
- [Specific recommendation 2 based on their concerns]
- [Specific recommendation 3 based on their concerns]

KEY_CONCERNS: [concern1, concern2, concern3]

RISK_LEVEL: {determined_risk}

REMEMBER: 
- Be specific to THEIR situation - no generic "it's okay to have ups and downs" when there are serious concerns
- Match your response to the severity level
- Acknowledge the hard reality of their struggles while offering hope and concrete support"""

    return prompt


def get_fallback_recommendations(risk_level: str, concerns: list, mood: int = 5, sleep: int = 5, activity: int = 5) -> dict:
    """
    Get fallback recommendations if Claude response parsing fails.
    
    Args:
        risk_level: The determined risk level
        concerns: List of identified concerns
        
    Returns:
        Dictionary with message and recommendations
    """
    
    if risk_level == "high":
        return {
            "message": "I'm concerned about what you're sharing. When multiple aspects of our wellbeing are struggling - especially mood, sleep, and medication - it's really important to reach out for support. You don't have to face this alone.",
            "recommendations": [
                "Please contact your healthcare provider or therapist today - this is important",
                "If you're feeling unsafe, call 988 (Suicide Prevention Lifeline) or text HOME to 741741",
                "Try to take your medication as prescribed - it's a crucial foundation for stability"
            ]
        }
    elif risk_level == "moderate":
        concern_specific = []
        if "missed_medication" in concerns:
            concern_specific.append("Set up medication reminders on your phone or pair it with a daily habit")
        if "low_mood" in concerns or "poor_sleep" in concerns:
            concern_specific.append("Reach out to a friend, family member, or therapist for support")
        if "poor_sleep" in concerns:
            concern_specific.append("Try a calming bedtime routine - avoid screens 30 minutes before bed")
        if "minimal_activity" in concerns:
            concern_specific.append("Start with just 10 minutes of gentle movement or a short walk")
        
        # Fill to 3 recommendations
        if len(concern_specific) < 3:
            concern_specific.append("Consider scheduling a check-in with your healthcare provider")
            
        return {
            "message": "I notice some concerning patterns in your check-in. When we're struggling with " + 
                      (" and ".join([c.replace("_", " ") for c in concerns[:2]])) +
                      ", it can feel overwhelming. Let's focus on some concrete steps to support you.",
            "recommendations": concern_specific[:3]
        }
    else:
        # LOW RISK - but differentiate between "doing great" vs "just okay"
        if "missed_medication" in concerns:
            return {
                "message": "You're doing great with your mood, sleep, and activity! However, I want to gently remind you about your medication. Even when we're feeling good, consistent medication helps maintain that stability long-term.",
                "recommendations": [
                    "Set up a daily medication reminder to help with consistency",
                    "Consider pairing medication with a daily habit (morning coffee, brushing teeth)",
                    "Keep up your excellent self-care - you're doing wonderfully!"
                ]
            }
        # Check if things are mediocre (5/10 range)
        elif any(c in concerns for c in ["mediocre_mood", "mediocre_sleep", "low_activity"]) or (mood <= 5 and sleep <= 5):
            return {
                "message": "I hear you - things feel kind of middle-of-the-road right now. You're maintaining stability, which is good, but there's room to feel better. Let's look at some gentle ways to boost your wellbeing.",
                "recommendations": [
                    "Try adding one small positive activity today - a short walk, calling a friend, or a hobby you enjoy",
                    "Focus on improving sleep quality - a consistent bedtime routine can make a big difference",
                    "Consider what might help lift your mood slightly - even small changes can help"
                ]
            }
        # Actually doing well (7+ across the board)
        else:
            return {
                "message": "It's wonderful that you're doing so well! Your mood, sleep, and activity levels show you're taking great care of yourself. Keep up this positive momentum!",
                "recommendations": [
                    "Continue your current healthy routines - consistency is key",
                    "Consider what's working well and how to maintain it",
                    "Stay connected with your support system"
                ]
            }
