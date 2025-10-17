"""
RAG Chatbot with LangChain and Ollama
Complete RAG pipeline with ChromaDB retrieval and Ollama LLM
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sentence_transformers import SentenceTransformer
import chromadb
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Load configuration
from config.settings import (
    CHROMA_PERSIST_DIR, EMBED_MODEL, OLLAMA_MODEL,
    OLLAMA_BASE_URL, TOP_K_RESULTS, COLLECTION_NAME
)


class RAGChatbot:
    """RAG-powered Customer Support Chatbot"""
    
    def __init__(self):
        """Initialize the RAG chatbot components"""
        print("Initializing RAG Chatbot...")
        
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
        
        # Check if vector store has documents
        collection_count = self.vectorstore._collection.count()
        if collection_count == 0:
            raise ValueError(
                f"Vector database is empty! Please run 'python build_vector_db.py' first."
            )
        print(f"Vector store loaded: {collection_count:,} documents")
        
        # Initialize Ollama LLM
        print(f"Connecting to Ollama: {OLLAMA_MODEL}")
        self.llm = Ollama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7
        )
        
        # Create custom prompt template
        self.prompt_template = PromptTemplate(
            template="""You are a helpful customer support assistant. Use the following context from past customer support conversations to answer the user's question. If you cannot find a relevant answer in the context, say so politely and offer general help.

Context from past support conversations:
{context}

User Question: {question}

Helpful Answer:""",
            input_variables=["context", "question"]
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": TOP_K_RESULTS}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )
        
        print("[OK] RAG Chatbot initialized successfully!\n")
    
    def query(self, question: str, return_sources: bool = False):
        """
        Query the RAG chatbot
        
        Args:
            question: User's question
            return_sources: Whether to return source documents
            
        Returns:
            dict with 'answer' and optionally 'sources'
        """
        try:
            # Run the QA chain
            result = self.qa_chain.invoke({"query": question})
            
            response = {
                "answer": result["result"],
                "question": question
            }
            
            if return_sources and "source_documents" in result:
                sources = []
                for i, doc in enumerate(result["source_documents"][:3], 1):
                    metadata = doc.metadata
                    sources.append({
                        "rank": i,
                        "company": metadata.get("company", "Unknown"),
                        "customer_query": metadata.get("customer_query", ""),
                        "support_response": metadata.get("support_response", ""),
                        "similarity": "High" if i == 1 else "Medium" if i == 2 else "Low"
                    })
                response["sources"] = sources
            
            return response
            
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "question": question,
                "error": True
            }
    
    def search_similar(self, query: str, k: int = 5):
        """
        Search for similar customer support conversations
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar conversations with metadata
        """
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            results = []
            
            for i, doc in enumerate(docs, 1):
                metadata = doc.metadata
                results.append({
                    "rank": i,
                    "company": metadata.get("company", "Unknown"),
                    "customer_query": metadata.get("customer_query", ""),
                    "support_response": metadata.get("support_response", ""),
                    "full_conversation": doc.page_content
                })
            
            return results
            
        except Exception as e:
            print(f"Error searching: {e}")
            return []


def test_chatbot():
    """Test the RAG chatbot with sample queries"""
    print("="*60)
    print("TESTING RAG CHATBOT")
    print("="*60)
    
    try:
        # Initialize chatbot
        chatbot = RAGChatbot()
        
        # Test queries
        test_queries = [
            "How do I reset my password?",
            "My payment failed, what should I do?",
            "I need help with my account",
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Q: {query}")
            print("="*60)
            
            result = chatbot.query(query, return_sources=True)
            
            print(f"\nA: {result['answer']}")
            
            if "sources" in result:
                print(f"\n📚 Top Sources:")
                for source in result["sources"]:
                    print(f"\n{source['rank']}. Company: {source['company']} | Similarity: {source['similarity']}")
                    print(f"   Customer: {source['customer_query'][:100]}...")
                    print(f"   Support: {source['support_response'][:100]}...")
        
        print(f"\n{'='*60}")
        print("[OK] Test completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print("\nMake sure:")
        print("1. Ollama is running: ollama serve")
        print("2. Model is available: ollama pull gpt-oss:20b")
        print("3. Vector DB is built: python build_vector_db.py")


if __name__ == "__main__":
    test_chatbot()

