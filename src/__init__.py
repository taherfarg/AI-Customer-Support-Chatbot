"""
AI Customer Support RAG Chatbot - Enhanced Edition
A production-ready RAG-powered customer support system with streaming and chat management
"""

__version__ = "2.0.0"
__author__ = "Taher Farg"
__description__ = "AI-powered customer support chatbot using RAG, Ollama, and ChromaDB with streaming & history"

from .rag_chatbot import RAGChatbot
from .voice_utils import VoiceHandler
from .streaming_rag import StreamingRAGChatbot
from .chat_manager import ChatManager

__all__ = ["RAGChatbot", "VoiceHandler", "StreamingRAGChatbot", "ChatManager"]

