"""
Simple test script to verify the MindPulse API is working.

Run this after starting the server with: python main.py
"""

import requests
import json
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


def print_response(response: requests.Response, title: str):
    """Pretty print API response."""
    print(f"\n{'=' * 60}")
    print(f"🧪 {title}")
    print(f"{'=' * 60}")
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print("\nResponse:")
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(response.text)


def test_root():
    """Test root endpoint."""
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Root Endpoint")


def test_health():
    """Test health check endpoint."""
    response = requests.get(f"{BASE_URL}/api/health")
    print_response(response, "Health Check")


def test_chat():
    """Test chat endpoint."""
    payload = {
        "message": "I've been feeling really anxious lately and can't sleep well. What should I do?",
        "use_rag": True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json=payload
    )
    print_response(response, "Chat Endpoint")
    
    return response.json().get("session_id")


def test_sentiment():
    """Test sentiment analysis endpoint."""
    payload = {
        "text": "I feel hopeless and worthless. I don't know what to do anymore."
    }
    
    response = requests.post(
        f"{BASE_URL}/api/analyze-sentiment",
        json=payload
    )
    print_response(response, "Sentiment Analysis")


def test_diagnosis():
    """Test diagnosis insights endpoint."""
    payload = {
        "symptoms": ["insomnia", "fatigue", "loss of appetite", "sadness"],
        "duration": "2 weeks",
        "additional_info": "These symptoms started after a stressful life event"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/diagnose",
        json=payload
    )
    print_response(response, "Diagnosis Insights")


def test_stats():
    """Test statistics endpoint."""
    response = requests.get(f"{BASE_URL}/api/stats")
    print_response(response, "Dataset Statistics")


def test_session_management(session_id: str):
    """Test session management endpoints."""
    # Get session history
    response = requests.get(f"{BASE_URL}/api/session/{session_id}")
    print_response(response, f"Session History - {session_id}")
    
    # Clear session
    response = requests.delete(f"{BASE_URL}/api/session/{session_id}")
    print_response(response, f"Clear Session - {session_id}")


def run_all_tests():
    """Run all API tests."""
    print("\n" + "=" * 60)
    print("🧠 MindPulse API Test Suite")
    print("=" * 60)
    
    try:
        # Basic endpoints
        test_root()
        test_health()
        test_stats()
        
        # Main functionality
        session_id = test_chat()
        test_sentiment()
        test_diagnosis()
        
        # Session management
        if session_id:
            test_session_management(session_id)
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the server is running with: python main.py")
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")


if __name__ == "__main__":
    run_all_tests()

