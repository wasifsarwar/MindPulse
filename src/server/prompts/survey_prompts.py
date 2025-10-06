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
- Recognizing discrepancies between physical and emotional wellbeing

CRITICAL GUIDELINES:
1. Be accurate and specific - don't minimize serious concerns
2. Match your tone to the severity level (don't be overly cheerful for concerning responses)
3. Provide actionable, evidence-based recommendations
4. Acknowledge specific issues mentioned by the user
5. Be empathetic but realistic - avoid generic platitudes when there are serious concerns
6. Recognize when physical health indicators don't match emotional state
7. NEVER be overly positive when mood is low, even if other factors are good

SEVERITY ASSESSMENT:
- LOW: All factors genuinely good (mood 7-10, sleep 7-10, active 6-10)
- MODERATE: 
  * Multiple mediocre factors (5-6 range)
  * Mood discrepancy (good sleep/activity but mood 4-6 - suggests underlying issues)
  * 1-2 critical concerns
  * Missed meds + other issues
- HIGH: 
  * Missed medication + very low mood (≤3)
  * 3+ critical factors
  * Severe discrepancy (excellent sleep/activity but mood ≤4)

SCORE INTERPRETATION:
- 8-10: Excellent/Great - celebrate and reinforce
- 6-7: Good/Stable - acknowledge positively but watch for discrepancies
- 5-6: Okay/Mediocre - acknowledge honestly, validate feeling stuck, provide encouragement
- 3-4: Concerning - need support and actionable steps
- 1-2: Critical - immediate intervention, crisis resources

IMPORTANT PATTERN RECOGNITION:

**Discrepancy Detection (HIGH PRIORITY):**
When sleep quality and/or physical activity are significantly higher (7-10) than mood (≤6), this is a RED FLAG:
- This suggests underlying mental health issues that lifestyle factors aren't addressing
- Physical health alone cannot fix chemical/psychological imbalances
- May indicate depression, anxiety, or other conditions requiring professional support
- Response should be concerned and recommend professional evaluation
- Example: Sleep 8-9, Activity 8, but Mood 4-5 → "I notice you're taking good care of your physical health, but your mood isn't reflecting that - this is important to address with a professional"

**Medication Adherence Context:**
- If medication missed BUT everything else is excellent → MODERATE risk (consistency matters)
- If medication missed AND other concerns present → HIGH risk (more serious intervention)

RESPONSE TONE BY SEVERITY:
- HIGH: Serious, supportive, directive - emphasize professional help
- MODERATE: Concerned, empathetic, constructive - acknowledge struggles honestly
- LOW: Genuinely positive and encouraging (only when things are actually going well)

**For "Okay" Feelings (5-6 range):**
- Don't dismiss with overly positive platitudes
- Acknowledge that "okay" is valid but not ideal
- Explore whether this is a plateau or subtle decline
- Provide gentle, realistic encouragement
- Validate that they deserve to feel better than just "okay\""""


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
    
    # Detect discrepancy between physical health and mood
    discrepancy_alert = ""
    physical_avg = (sleep_quality + physical_activity) / 2
    mood_physical_gap = physical_avg - mood_rating
    
    if physical_avg >= 7 and mood_rating <= 6:
        discrepancy_alert = f"""
⚠️ CRITICAL DISCREPANCY DETECTED:
Physical health indicators (Sleep: {sleep_quality}, Activity: {physical_activity}) are MUCH better than mood ({mood_rating}).
This suggests underlying mental health issues that lifestyle factors alone aren't addressing.
This person may need professional mental health support - physical health alone cannot resolve this."""
    elif physical_avg >= 6 and mood_rating <= 4:
        discrepancy_alert = f"""
⚠️ SEVERE DISCREPANCY DETECTED:
Despite adequate sleep ({sleep_quality}) and activity ({physical_activity}), mood is very low ({mood_rating}).
This is a red flag for depression or other mental health conditions requiring professional evaluation."""
    
    # Build context about severity
    severity_context = f"""
CALCULATED RISK LEVEL: {determined_risk.upper()}
IDENTIFIED CONCERNS: {', '.join(concerns) if concerns else 'None'}
{discrepancy_alert}

ASSESSMENT CONTEXT:
- Medication adherence: {'✓ Taken' if medication_taken else '✗ MISSED (concerning)'}
- Mood: {mood_rating}/10 {'(CRITICAL - very low)' if mood_rating <= 3 else '(concerning - low)' if mood_rating <= 5 else '(mediocre - just okay)' if mood_rating == 6 else '(stable)' if mood_rating <= 7 else '(good)'}
- Sleep: {sleep_quality}/10 {'(CRITICAL - very poor)' if sleep_quality <= 3 else '(concerning)' if sleep_quality <= 5 else '(mediocre - just okay)' if sleep_quality == 6 else '(stable)' if sleep_quality <= 7 else '(good)'}
- Activity: {physical_activity}/10 {'(CRITICAL - minimal)' if physical_activity <= 2 else '(low)' if physical_activity <= 5 else '(mediocre - just okay)' if physical_activity == 6 else '(moderate)' if physical_activity <= 7 else '(good)'}
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

KEY_CONCERNS: concern1, concern2, concern3

RISK_LEVEL: {determined_risk}

NOTE: Do NOT include square brackets [] around the KEY_CONCERNS list - just provide comma-separated values.

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
        mood: Mood rating (for better contextual responses)
        sleep: Sleep quality (for better contextual responses)
        activity: Physical activity (for better contextual responses)
        
    Returns:
        Dictionary with message and recommendations
    """
    
    # Check for discrepancies
    physical_avg = (sleep + activity) / 2
    has_discrepancy = physical_avg >= 7 and mood <= 6
    has_severe_discrepancy = physical_avg >= 6 and mood <= 4
    
    if risk_level == "high":
        if has_severe_discrepancy:
            return {
                "message": f"I'm noticing something important: you're taking good care of your physical health (sleep: {sleep}/10, activity: {activity}/10), but your mood is {mood}/10. When physical health is good but mood remains low, it often points to underlying mental health issues that need professional attention. This isn't something lifestyle changes alone can fix.",
                "recommendations": [
                    "Please schedule an appointment with a mental health professional - this discrepancy is significant",
                    "If you have a therapist or psychiatrist, let them know about this pattern as soon as possible",
                    "If you're feeling unsafe or having dark thoughts, call 988 (Suicide Prevention Lifeline) immediately"
                ]
            }
        else:
            return {
                "message": "I'm concerned about what you're sharing. When multiple aspects of our wellbeing are struggling - especially mood, sleep, and medication - it's really important to reach out for support. You don't have to face this alone.",
                "recommendations": [
                    "Please contact your healthcare provider or therapist today - this is important",
                    "If you're feeling unsafe, call 988 (Suicide Prevention Lifeline) or text HOME to 741741",
                    "Try to take your medication as prescribed - it's a crucial foundation for stability"
                ]
            }
    elif risk_level == "moderate":
        if has_discrepancy:
            return {
                "message": f"I notice you're maintaining good physical habits (sleep: {sleep}/10, activity: {activity}/10), but your mood is at {mood}/10. This suggests your physical health isn't translating to emotional wellbeing, which is worth exploring with professional support. There may be underlying factors that need attention.",
                "recommendations": [
                    "Consider scheduling a session with a therapist or counselor to explore what's affecting your mood",
                    "Keep track of this pattern - note when physical health is good but mood stays low",
                    "Don't dismiss your feelings just because you're 'doing everything right' - your mood matters"
                ]
            }
        
        concern_specific = []
        if "missed_medication" in concerns:
            concern_specific.append("Set up medication reminders on your phone or pair it with a daily habit")
        if "low_mood" in concerns or "mediocre_mood" in concerns:
            concern_specific.append("Reach out to a friend, family member, or therapist for support")
        if "poor_sleep" in concerns or "mediocre_sleep" in concerns:
            concern_specific.append("Try a calming bedtime routine - avoid screens 30 minutes before bed")
        if "minimal_activity" in concerns or "low_activity" in concerns:
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
        # Check if things are "just okay" (6 range)
        elif mood == 6 or "okay_mood" in concerns:
            return {
                "message": f"You're feeling 'okay' (mood: {mood}/10), which is valid - but I wonder if there's room to feel better. You're maintaining stability, and that's worth acknowledging. Let's explore some gentle ways to move from 'okay' to 'good.'",
                "recommendations": [
                    "Reflect on what might help shift from 'okay' to 'good' - sometimes small changes make a difference",
                    "Consider whether 'okay' is a plateau or a subtle decline - trust your instincts",
                    "You deserve to feel better than just 'okay' - explore what that might look like for you"
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
