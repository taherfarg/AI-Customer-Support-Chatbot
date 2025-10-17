"""
Setup Verification Script
Checks if all prerequisites are met before building the RAG chatbot
"""

import sys
import os
from pathlib import Path

def check_data_file():
    """Check if cleaned dataset exists"""
    data_files = [
        Path("data/customer_support_qa_clean.csv"),
        Path("customer_support_qa_clean.csv")
    ]
    
    for data_file in data_files:
        if data_file.exists():
            print(f"[OK] Found: {data_file}")
            return True
    
    print(f"[X] Missing: data/customer_support_qa_clean.csv")
    print("   Please run the notebook 'data/explor_the_data_set.ipynb' to generate it.")
    return False

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        import ollama
        # Try to list models
        models = ollama.list()
        print("[OK] Ollama is installed and running")
        
        # Check if gpt-oss:20b is available
        model_names = [m['name'] for m in models.get('models', [])]
        if any('gpt-oss' in name for name in model_names):
            print("[OK] gpt-oss:20b model found")
            return True
        else:
            print("[WARN] gpt-oss:20b not found in Ollama")
            print("       Run: ollama pull gpt-oss:20b")
            return False
    except ImportError:
        print("[X] Ollama Python package not installed")
        print("   Run: pip install ollama")
        return False
    except Exception as e:
        print(f"[X] Ollama error: {e}")
        print("   Make sure Ollama is running (ollama serve)")
        return False

def check_dependencies():
    """Check if all Python packages are installed"""
    required = [
        'chromadb',
        'sentence_transformers',
        'langchain',
        'gradio',
        'pandas',
        'numpy',
        'tqdm'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"[OK] {package}")
        except ImportError:
            print(f"[X] {package}")
            missing.append(package)
    
    if missing:
        print(f"\n[X] Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("="*60)
    print("RAG CHATBOT SETUP VERIFICATION")
    print("="*60)
    
    print("\nChecking Dependencies...")
    deps_ok = check_dependencies()
    
    print("\nChecking Data Files...")
    data_ok = check_data_file()
    
    print("\nChecking Ollama & Model...")
    ollama_ok = check_ollama()
    
    print("\n" + "="*60)
    if deps_ok and data_ok and ollama_ok:
        print("[PASS] ALL CHECKS PASSED! Ready to build RAG chatbot.")
        return 0
    else:
        print("[FAIL] SOME CHECKS FAILED. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

