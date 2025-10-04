"""Quick test to see if imports work."""

import sys
print("Testing imports...")

try:
    print("1. Importing config...")
    from config import settings, validate_settings
    print("   ✅ Config imported")
    
    print("2. Validating settings...")
    validate_settings()
    print("   ✅ Settings validated")
    
    print("3. Importing API...")
    from api import create_app
    print("   ✅ API imported")
    
    print("4. Creating app...")
    app = create_app()
    print("   ✅ App created successfully!")
    
    print("\n✅ All imports successful! Server should work.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
