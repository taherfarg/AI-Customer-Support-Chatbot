"""
AI Customer Support RAG Chatbot
A production-ready RAG-powered customer support system
"""

__version__ = "1.0.0"
__author__ = "Taher Farg"
__description__ = "AI-powered customer support chatbot using RAG, Ollama, and ChromaDB"

from .rag_chatbot import RAGChatbot
from .voice_utils import VoiceHandler

__all__ = ["RAGChatbot", "VoiceHandler"]

