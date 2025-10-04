"""Test the live server to see what API key it's using."""

import requests

# Test if server is running
try:
    response = requests.post(
        "http://localhost:8000/api/chat",
        json={"message": "test", "use_rag": False},
        timeout=5
    )
    
    result = response.json()
    
    if "error" in result:
        print("❌ Server returned error:", result.get("error", "")[:200])
    elif "I apologize" in result.get("response", ""):
        print("❌ Server got 401 authentication error")
        print("This means the server has a bad API key cached")
        print("\n🔧 FIX: You MUST restart the server!")
        print("   1. Find the terminal running 'python3 main.py'")
        print("   2. Press Ctrl+C to stop it")
        print("   3. Run 'python3 main.py' again")
    else:
        print("✅ Server is working! Claude responded:")
        print(f"   {result.get('response', '')[:100]}...")
        
except requests.exceptions.ConnectionError:
    print("❌ Server is not running on port 8000")
    print("\n🔧 FIX: Start the server:")
    print("   cd /Users/wasifsmacbookpro/Desktop/Oct-4-Hackathon-2025-/submissions/MindPulse")
    print("   python3 main.py")
except Exception as e:
    print(f"❌ Error: {e}")
