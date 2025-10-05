"""Test all risk level scenarios to ensure accurate analysis."""

import requests
import json

def test_scenario(name, data):
    """Test a single scenario."""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    print(f"Medication: {'Yes' if data['medication_taken'] else 'No'}")
    print(f"Mood: {data['mood_rating']}/10")
    print(f"Sleep: {data['sleep_quality']}/10")
    print(f"Activity: {data['physical_activity']}/10")
    print(f"Thoughts: \"{data['thoughts']}\"")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8000/api/analyze-survey",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ RISK LEVEL: {result['risk_level'].upper()}")
            print(f"📞 Provider Contacted: {result['provider_contacted']}")
            print(f"⚠️  Key Concerns: {', '.join(result['key_concerns']) if result['key_concerns'] else 'None'}")
            print()
            print(f"💬 Message: {result['message'][:120]}...")
            print()
            print(f"📋 Recommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"   {i}. {rec}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Test Cases
print("\n" + "="*70)
print("MINDPULSE ANALYSIS ACCURACY TEST")
print("="*70)

# 1. HIGH RISK - Critical mood + missed medication
test_scenario(
    "HIGH RISK - Missed medication + very low mood",
    {
        "medication_taken": False,
        "mood_rating": 2,
        "sleep_quality": 6,
        "physical_activity": 5,
        "thoughts": "I forgot my medication and feel hopeless today"
    }
)

# 2. HIGH RISK - Multiple critical factors
test_scenario(
    "HIGH RISK - Multiple critical factors",
    {
        "medication_taken": False,
        "mood_rating": 2,
        "sleep_quality": 2,
        "physical_activity": 1,
        "thoughts": "Everything feels overwhelming and I can't sleep"
    }
)

# 3. MODERATE RISK - Missed medication + concerning mood
test_scenario(
    "MODERATE RISK - Missed medication + concerning mood",
    {
        "medication_taken": False,
        "mood_rating": 5,
        "sleep_quality": 7,
        "physical_activity": 6,
        "thoughts": "Forgot my meds this morning, feeling a bit off"
    }
)

# 4. MODERATE RISK - Low mood + poor sleep (but took meds)
test_scenario(
    "MODERATE RISK - Low mood + poor sleep",
    {
        "medication_taken": True,
        "mood_rating": 4,
        "sleep_quality": 3,
        "physical_activity": 4,
        "thoughts": "Struggling to sleep and feeling down"
    }
)

# 5. LOW RISK - Good overall
test_scenario(
    "LOW RISK - Healthy check-in",
    {
        "medication_taken": True,
        "mood_rating": 8,
        "sleep_quality": 8,
        "physical_activity": 7,
        "thoughts": "Feeling pretty good today, had a productive day"
    }
)

# 6. LOW RISK - One minor concern
test_scenario(
    "LOW RISK - One minor concern (slight fatigue)",
    {
        "medication_taken": True,
        "mood_rating": 7,
        "sleep_quality": 6,
        "physical_activity": 4,
        "thoughts": "Good mood but feeling a bit tired lately"
    }
)

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)

