"""Test the survey analysis endpoint."""

import requests
import json

BASE_URL = "http://localhost:8000"

# Example survey responses
survey_data = {
    "medication_taken": False,  # Missed medication
    "mood_rating": 4,            # Low mood
    "sleep_quality": 3,          # Poor sleep
    "physical_activity": 2,      # Low activity
    "thoughts": "I've been feeling really overwhelmed with work and can't seem to catch up. It's affecting my sleep and I keep forgetting to take my medication."
}

print("🧪 Testing Survey Analysis Endpoint")
print("=" * 60)
print(f"\n📋 Survey Responses:")
print(f"  • Medication taken: {survey_data['medication_taken']}")
print(f"  • Mood: {survey_data['mood_rating']}/10")
print(f"  • Sleep quality: {survey_data['sleep_quality']}/10")
print(f"  • Physical activity: {survey_data['physical_activity']}/10")
print(f"  • Thoughts: {survey_data['thoughts'][:60]}...")
print()

try:
    response = requests.post(
        f"{BASE_URL}/api/analyze-survey",
        json=survey_data,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ Response received:")
        print(f"\n💬 Message:")
        print(f"   {result['message']}")
        
        print(f"\n📝 Recommendations:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n⚠️  Key Concerns: {', '.join(result['key_concerns']) if result['key_concerns'] else 'None identified'}")
        print(f"\n🎯 Risk Level: {result['risk_level'].upper()}")
        
    else:
        print(f"❌ Error: Status code {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Error: Could not connect to server")
    print("   Make sure the server is running:")
    print("   cd src/server && python3 main.py")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)

