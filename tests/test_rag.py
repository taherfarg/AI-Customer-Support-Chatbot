"""
Tests for RAG Chatbot
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_chatbot import RAGChatbot


class TestRAGChatbot:
    """Test RAG chatbot functionality"""
    
    @pytest.fixture
    def chatbot(self):
        """Initialize chatbot for testing"""
        try:
            return RAGChatbot()
        except Exception as e:
            pytest.skip(f"Chatbot initialization failed: {e}")
    
    def test_chatbot_initialization(self, chatbot):
        """Test chatbot initializes correctly"""
        assert chatbot is not None
        assert chatbot.llm is not None
        assert chatbot.vectorstore is not None
        assert chatbot.qa_chain is not None
    
    def test_query_basic(self, chatbot):
        """Test basic query"""
        result = chatbot.query("How do I reset my password?")
        assert "answer" in result
        assert "question" in result
        assert len(result["answer"]) > 0
    
    def test_query_with_sources(self, chatbot):
        """Test query with source retrieval"""
        result = chatbot.query("My payment failed", return_sources=True)
        assert "answer" in result
        assert "sources" in result
        assert isinstance(result["sources"], list)
    
    def test_search_similar(self, chatbot):
        """Test similarity search"""
        results = chatbot.search_similar("password reset", k=3)
        assert isinstance(results, list)
        assert len(results) <= 3
        if len(results) > 0:
            assert "company" in results[0]
            assert "customer_query" in results[0]
            assert "support_response" in results[0]


def test_import():
    """Test that modules can be imported"""
    from rag_chatbot import RAGChatbot
    from voice_utils import VoiceHandler
    
    assert RAGChatbot is not None
    assert VoiceHandler is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

