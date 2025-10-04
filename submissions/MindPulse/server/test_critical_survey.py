"""Test survey endpoint with critical responses that should trigger provider alert."""

import requests
import json

def test_critical_responses():
    """Test responses that SHOULD trigger provider alert."""
    
    print("=" * 70)
    print("Testing Critical Survey Responses (Should Alert Provider)")
    print("=" * 70)
    print()
    
    # This should trigger alert: low mood + no medication
    test_case_1 = {
        "medication_taken": False,
        "mood_rating": 2,
        "sleep_quality": 6,
        "physical_activity": 5,
        "thoughts": "Feeling really hopeless today"
    }
    
    print("TEST CASE 1: Critical mood + missed medication")
    print(f"  Medication: {'Yes' if test_case_1['medication_taken'] else 'No'}")
    print(f"  Mood: {test_case_1['mood_rating']}/10")
    print(f"  Sleep: {test_case_1['sleep_quality']}/10")
    print(f"  Activity: {test_case_1['physical_activity']}/10")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8000/api/analyze-survey",
            json=test_case_1,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Response received:")
            print(f"  Risk Level: {data.get('risk_level', 'N/A')}")
            print(f"  Provider Contacted: {data.get('provider_contacted', False)}")
            print(f"  Key Concerns: {', '.join(data.get('key_concerns', []))}")
            print()
            print(f"  Message: {data.get('message', '')[:100]}...")
            print()
            
            if data.get('provider_contacted'):
                print("🚨 ALERT TRIGGERED - Provider should be notified!")
            else:
                print("⚠️  NO ALERT - Provider not contacted")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 70)
    print()
    
    # Test case 2: Multiple concerning factors
    test_case_2 = {
        "medication_taken": False,
        "mood_rating": 2,
        "sleep_quality": 2,
        "physical_activity": 1,
        "thoughts": "Everything feels overwhelming and I can't cope"
    }
    
    print("TEST CASE 2: Multiple critical factors (should definitely alert)")
    print(f"  Medication: {'Yes' if test_case_2['medication_taken'] else 'No'}")
    print(f"  Mood: {test_case_2['mood_rating']}/10")
    print(f"  Sleep: {test_case_2['sleep_quality']}/10")
    print(f"  Activity: {test_case_2['physical_activity']}/10")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8000/api/analyze-survey",
            json=test_case_2,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Response received:")
            print(f"  Risk Level: {data.get('risk_level', 'N/A')}")
            print(f"  Provider Contacted: {data.get('provider_contacted', False)}")
            print(f"  Key Concerns: {', '.join(data.get('key_concerns', []))}")
            print()
            
            if data.get('provider_contacted'):
                print("🚨 ALERT TRIGGERED - Provider should be notified!")
            else:
                print("⚠️  NO ALERT - Provider not contacted")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 70)
    print("Alert Criteria Reminder:")
    print("=" * 70)
    print("Alerts trigger when:")
    print("  • Mood ≤ 3 + Medication NOT taken, OR")
    print("  • 3+ concerning factors (mood ≤3, sleep ≤3, no med, activity ≤2), OR")
    print("  • High risk + 2+ factors")
    print("=" * 70)

if __name__ == "__main__":
    test_critical_responses()
