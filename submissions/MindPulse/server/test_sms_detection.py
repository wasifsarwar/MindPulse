"""Test script for SMS deterioration detection logic."""

from utils.sms import is_deterioration_detected

def test_scenarios():
    """Test various scenarios to see when alerts trigger."""
    
    print("=" * 60)
    print("Testing MindPulse Deterioration Detection")
    print("=" * 60)
    print()
    
    scenarios = [
        {
            "name": "Healthy Response",
            "medication_taken": True,
            "mood_rating": 8,
            "sleep_quality": 7,
            "physical_activity": 6,
            "risk_level": "low"
        },
        {
            "name": "Slightly Concerning",
            "medication_taken": True,
            "mood_rating": 5,
            "sleep_quality": 5,
            "physical_activity": 4,
            "risk_level": "low"
        },
        {
            "name": "Moderate Risk - Missed Medication",
            "medication_taken": False,
            "mood_rating": 4,
            "sleep_quality": 4,
            "physical_activity": 3,
            "risk_level": "moderate"
        },
        {
            "name": "High Risk - Multiple Factors",
            "medication_taken": False,
            "mood_rating": 2,
            "sleep_quality": 2,
            "physical_activity": 1,
            "risk_level": "high"
        },
        {
            "name": "Critical - Low Mood + No Medication",
            "medication_taken": False,
            "mood_rating": 2,
            "sleep_quality": 5,
            "physical_activity": 5,
            "risk_level": "moderate"
        },
        {
            "name": "Borderline - 2 factors",
            "medication_taken": False,
            "mood_rating": 3,
            "sleep_quality": 6,
            "physical_activity": 5,
            "risk_level": "low"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        name = scenario.pop("name")
        alert = is_deterioration_detected(**scenario)
        
        print(f"{i}. {name}")
        print(f"   Medication: {'✓' if scenario['medication_taken'] else '✗'}")
        print(f"   Mood: {scenario['mood_rating']}/10")
        print(f"   Sleep: {scenario['sleep_quality']}/10")
        print(f"   Activity: {scenario['physical_activity']}/10")
        print(f"   Risk: {scenario['risk_level']}")
        print(f"   → Alert Provider: {'🚨 YES' if alert else '✓ No'}")
        print()
    
    print("=" * 60)
    print("Summary of Alert Criteria:")
    print("=" * 60)
    print("✗ Medication not taken")
    print("✗ Mood ≤ 3 (critical)")
    print("✗ Sleep ≤ 3 (critical)")
    print("✗ Activity ≤ 2 (minimal)")
    print()
    print("Alerts trigger when:")
    print("• 3+ concerning factors, OR")
    print("• High risk + 2+ factors, OR")
    print("• Critical mood + no medication")
    print("=" * 60)

if __name__ == "__main__":
    test_scenarios()
