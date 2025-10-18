"""
Streaming RAG Chatbot
Enhanced version with streaming response support
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.callbacks.base import BaseCallbackHandler

# Load configuration
from config.settings import (
    CHROMA_PERSIST_DIR, EMBED_MODEL, OLLAMA_MODEL,
    OLLAMA_BASE_URL, TOP_K_RESULTS, COLLECTION_NAME
)


class StreamingCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming tokens"""
    
    def __init__(self):
        self.tokens = []
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when LLM generates a new token"""
        self.tokens.append(token)
        print(token, end="", flush=True)


class StreamingRAGChatbot:
    """RAG Chatbot with streaming support and conversation context"""
    
    def __init__(self):
        """Initialize the streaming RAG chatbot"""
        print("Initializing Streaming RAG Chatbot...")
        
        # Initialize embedding model
        print(f"Loading embedding model: {EMBED_MODEL}")
        self.embeddings = SentenceTransformerEmbeddings(
            model_name=EMBED_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize ChromaDB vector store
        print(f"Connecting to ChromaDB: {CHROMA_PERSIST_DIR}")
        self.vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )
        
        # Get collection info
        collection_count = self.vectorstore._collection.count()
        print(f"Vector store loaded: {collection_count:,} documents")
        
        # Initialize Ollama LLM with streaming
        print(f"Connecting to Ollama: {OLLAMA_MODEL}")
        self.llm = Ollama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7,
            streaming=True  # Enable streaming
        )
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": TOP_K_RESULTS}
        )
        
        # Create prompt template with conversation context
        self.prompt_template = PromptTemplate(
            template="""You are a helpful AI customer support assistant. Use the following context from previous customer support conversations to answer the question.

Previous Conversation:
{conversation_history}

Context from knowledge base:
{context}

Current Question: {question}

Provide a helpful, accurate, and professional response based on the context above. If the context doesn't contain relevant information, say so and provide general guidance.

Answer:""",
            input_variables=["conversation_history", "context", "question"]
        )
        
        print("[OK] Streaming RAG Chatbot initialized successfully!\n")
    
    def query(self, question: str, conversation_history: str = "", return_sources: bool = False):
        """
        Query the RAG chatbot with streaming support
        
        Args:
            question: User's question
            conversation_history: Previous conversation context
            return_sources: Whether to return source documents
            
        Returns:
            Generator yielding response chunks or dict with full response
        """
        try:
            # Search for relevant documents
            docs = self.retriever.get_relevant_documents(question)
            
            # Prepare context
            context = "\n\n".join([
                f"Company: {doc.metadata.get('company', 'Unknown')}\n"
                f"Customer: {doc.metadata.get('customer_query', 'N/A')}\n"
                f"Support: {doc.metadata.get('support_response', 'N/A')}"
                for doc in docs
            ])
            
            # Format the prompt
            formatted_prompt = self.prompt_template.format(
                conversation_history=conversation_history or "No previous conversation.",
                context=context,
                question=question
            )
            
            # Generate response with streaming
            streaming_handler = StreamingCallbackHandler()
            
            response = self.llm.invoke(
                formatted_prompt,
                callbacks=[streaming_handler]
            )
            
            # Prepare result
            result = {
                "question": question,
                "answer": response
            }
            
            # Add sources if requested
            if return_sources:
                sources = []
                for i, doc in enumerate(docs, 1):
                    sources.append({
                        "rank": i,
                        "company": doc.metadata.get("company", "Unknown"),
                        "customer_query": doc.metadata.get("customer_query", "N/A"),
                        "support_response": doc.metadata.get("support_response", "N/A"),
                        "similarity": doc.metadata.get("similarity", "N/A")
                    })
                result["sources"] = sources
            
            return result
            
        except Exception as e:
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "error": True
            }
    
    def query_stream(self, question: str, conversation_history: str = ""):
        """
        Query with streaming response (generator)
        
        Args:
            question: User's question
            conversation_history: Previous conversation context
            
        Yields:
            Response tokens as they're generated
        """
        try:
            # Search for relevant documents
            docs = self.retriever.get_relevant_documents(question)
            
            # Prepare context
            context = "\n\n".join([
                f"Company: {doc.metadata.get('company', 'Unknown')}\n"
                f"Customer: {doc.metadata.get('customer_query', 'N/A')}\n"
                f"Support: {doc.metadata.get('support_response', 'N/A')}"
                for doc in docs
            ])
            
            # Format the prompt
            formatted_prompt = self.prompt_template.format(
                conversation_history=conversation_history or "No previous conversation.",
                context=context,
                question=question
            )
            
            # Stream the response
            for chunk in self.llm.stream(formatted_prompt):
                yield chunk
                
        except Exception as e:
            yield f"\n\n[ERROR] {str(e)}"
    
    def search_similar(self, query: str, k: int = 5):
        """
        Search for similar customer support conversations
        
        Args:
            query: Search query
            k: Number of results
            
        Returns:
            List of similar conversations
        """
        docs = self.retriever.get_relevant_documents(query)[:k]
        
        results = []
        for doc in docs:
            results.append({
                "company": doc.metadata.get("company", "Unknown"),
                "customer_query": doc.metadata.get("customer_query", "N/A"),
                "support_response": doc.metadata.get("support_response", "N/A"),
            })
        
        return results


if __name__ == "__main__":
    """Test the streaming chatbot"""
    print("="*60)
    print("TESTING STREAMING RAG CHATBOT")
    print("="*60)
    
    try:
        # Initialize chatbot
        chatbot = StreamingRAGChatbot()
        
        # Test query
        test_question = "How do I reset my password?"
        print(f"\n\nQuestion: {test_question}")
        print("\nStreaming Answer:\n")
        
        full_response = ""
        for chunk in chatbot.query_stream(test_question):
            full_response += chunk
        
        print(f"\n\n{'='*60}")
        print("[OK] Test completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print("\nMake sure:")
        print("1. Ollama is running: ollama serve")
        print("2. Model is available: ollama pull gpt-oss:20b")
        print("3. Vector DB is built: python scripts/build_vector_db.py")

