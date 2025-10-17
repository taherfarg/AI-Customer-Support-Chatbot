"""
Configuration Settings
Centralized configuration management
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Data Configuration
DATA_FILE = str(DATA_DIR / "customer_support_qa_clean.csv")

# Vector Database Configuration
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(PROJECT_ROOT / "chroma_db"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "customer_support_qa")
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))

# Model Configuration
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
OLLAMA_MODEL = os.getenv("MODEL_NAME", "gpt-oss:20b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Embedding Configuration
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "128"))
MAX_ROWS = os.getenv("MAX_ROWS", None)
if MAX_ROWS:
    MAX_ROWS = int(MAX_ROWS)
FORCE_CPU = os.getenv("FORCE_CPU", "true").lower() == "true"

# Gradio Configuration
GRADIO_PORT = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "false").lower() == "true"

# Voice Configuration
VOICE_ENABLED = os.getenv("VOICE_ENABLED", "true").lower() == "true"
TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "en")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = str(LOGS_DIR / "chatbot.log")

# Application Metadata
APP_NAME = "AI Customer Support Chatbot"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "RAG-powered customer support chatbot with voice capabilities"

