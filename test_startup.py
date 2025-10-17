"""
Test script to diagnose app startup issues
"""

print("=" * 60)
print("TESTING APP STARTUP")
print("=" * 60)

# Test 1: Import sys and path setup
print("\n[1/5] Testing imports...")
try:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    print("[OK] System imports OK")
except Exception as e:
    print(f"[ERROR] System imports failed: {e}")
    sys.exit(1)

# Test 2: Import configuration
print("\n[2/5] Testing configuration...")
try:
    from config.settings import *
    print(f"[OK] Configuration loaded")
    print(f"   - Model: {OLLAMA_MODEL}")
    print(f"   - Port: {GRADIO_PORT}")
    print(f"   - Vector DB: {CHROMA_PERSIST_DIR}")
except Exception as e:
    print(f"[ERROR] Configuration failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Import chatbot
print("\n[3/5] Testing RAG chatbot import...")
try:
    from rag_chatbot import RAGChatbot
    print("[OK] RAGChatbot imported")
except Exception as e:
    print(f"[ERROR] RAGChatbot import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Import voice handler
print("\n[4/5] Testing voice handler import...")
try:
    from voice_utils import VoiceHandler
    print("[OK] VoiceHandler imported")
except Exception as e:
    print(f"[ERROR] VoiceHandler import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Initialize chatbot
print("\n[5/5] Testing chatbot initialization...")
try:
    print("   Initializing... (this may take a minute)")
    chatbot = RAGChatbot()
    print("[OK] RAGChatbot initialized successfully!")
except Exception as e:
    print(f"[ERROR] RAGChatbot initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] ALL TESTS PASSED! App should work.")
print("=" * 60)
print(f"\nYou can now run: python app.py")
print(f"Then open: http://localhost:{GRADIO_PORT}")

