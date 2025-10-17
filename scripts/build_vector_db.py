"""
Build Vector Database (GPU-Accelerated)
Loads cleaned customer support Q&A data and creates ChromaDB collection with embeddings
Uses GPU acceleration for fast embedding generation if available
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from tqdm import tqdm

# Load configuration
from config.settings import (
    DATA_FILE, CHROMA_PERSIST_DIR, EMBED_MODEL,
    COLLECTION_NAME, BATCH_SIZE, MAX_ROWS, FORCE_CPU
)

def check_gpu():
    """Check GPU availability without explicit torch import"""
    if FORCE_CPU:
        print("[INFO] Forced CPU mode (FORCE_CPU=True)")
        print("[INFO] Change FORCE_CPU=False to enable GPU if compatible")
        return 'cpu'
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            gpu_compute = torch.cuda.get_device_capability(0)
            print(f"[GPU] {gpu_name}")
            print(f"[GPU] Memory: {gpu_memory:.2f} GB")
            print(f"[GPU] Compute Capability: sm_{gpu_compute[0]}{gpu_compute[1]}")
            print(f"[GPU] CUDA Version: {torch.version.cuda}")
            
            # Check if GPU is compatible (sm75+ recommended)
            if gpu_compute[0] < 7 or (gpu_compute[0] == 7 and gpu_compute[1] < 5):
                print(f"[WARN] Old GPU architecture detected (sm{gpu_compute[0]}{gpu_compute[1]})")
                print(f"[WARN] Falling back to CPU to avoid CUDA kernel errors")
                return 'cpu'
            
            return 'cuda'
        else:
            print("[INFO] GPU not available, using CPU")
            return 'cpu'
    except Exception as e:
        print(f"[INFO] GPU check failed: {e}")
        print("[INFO] Using CPU mode")
        return 'cpu'

def load_data():
    """Load cleaned Q&A dataset"""
    print(f"\nLoading data from {DATA_FILE}...")
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(
            f"{DATA_FILE} not found. Please run 'explor_the_data_set.ipynb' first."
        )
    
    df = pd.read_csv(DATA_FILE)
    
    # Limit dataset size if MAX_ROWS is set
    if MAX_ROWS is not None and len(df) > MAX_ROWS:
        print(f"[INFO] Limiting dataset to {MAX_ROWS} rows for faster processing")
        df = df.head(MAX_ROWS)
    
    print(f"Loaded {len(df)} Q&A pairs")
    print(f"Companies: {df['company'].nunique()}")
    return df

def initialize_embedding_model(device):
    """Initialize sentence transformer model with device support"""
    print(f"\nInitializing embedding model: {EMBED_MODEL}")
    print(f"Device: {device.upper()}")
    
    # Force CPU mode if device is 'cpu' to avoid any GPU issues
    if device == 'cpu':
        model = SentenceTransformer(EMBED_MODEL, device='cpu')
    else:
        model = SentenceTransformer(EMBED_MODEL, device=device)
    
    print(f"Model loaded successfully")
    print(f"Embedding dimension: {model.get_sentence_embedding_dimension()}")
    
    return model

def initialize_chromadb():
    """Initialize ChromaDB client with persistent storage"""
    print(f"\nInitializing ChromaDB...")
    print(f"Persist directory: {CHROMA_PERSIST_DIR}")
    
    # Create directory if it doesn't exist
    os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
    
    # Initialize persistent client
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    
    # Delete existing collection if it exists (for clean rebuild)
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except:
        pass
    
    # Create new collection
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Customer support Q&A embeddings"}
    )
    print(f"Created collection: {COLLECTION_NAME}")
    
    return client, collection

def build_vector_db(df, model, collection, device):
    """Generate embeddings and populate ChromaDB using available hardware"""
    print(f"\nBuilding vector database...")
    print(f"Processing {len(df)} Q&A pairs in batches of {BATCH_SIZE}")
    
    if device == 'cuda':
        est_time = len(df) // BATCH_SIZE // 10
        print(f"Estimated time: ~{est_time} seconds with GPU")
    else:
        est_time = len(df) // BATCH_SIZE * 2
        print(f"Estimated time: ~{est_time // 60} minutes on CPU")
    
    # Prepare data for batching
    total_batches = (len(df) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_idx in tqdm(range(0, len(df), BATCH_SIZE), total=total_batches, desc="Embedding batches"):
        batch_df = df.iloc[batch_idx:batch_idx + BATCH_SIZE]
        
        # Prepare batch data
        documents = []
        metadatas = []
        ids = []
        customer_inputs = []
        
        for idx, row in batch_df.iterrows():
            customer_input = str(row['input'])
            support_response = str(row['response'])
            company = str(row['company'])
            conv_id = str(row['conversation_id'])
            
            # Document to store (the full conversation context)
            document = f"Customer: {customer_input}\nSupport: {support_response}"
            
            # Metadata for filtering and context
            metadata = {
                "company": company,
                "conversation_id": conv_id,
                "customer_query": customer_input,
                "support_response": support_response
            }
            
            documents.append(document)
            metadatas.append(metadata)
            ids.append(f"qa_{idx}")
            customer_inputs.append(customer_input)
        
        # Generate embeddings for entire batch at once
        # sentence-transformers will automatically use GPU if available
        try:
            embeddings = model.encode(
                customer_inputs,
                convert_to_tensor=False,
                show_progress_bar=False,
                batch_size=BATCH_SIZE
            )
        except Exception as e:
            # Fallback to smaller batch if memory issues
            print(f"\n[WARN] Batch encoding failed, using smaller batches: {e}")
            embeddings = model.encode(
                customer_inputs,
                convert_to_tensor=False,
                show_progress_bar=False,
                batch_size=32
            )
        
        # Add batch to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings.tolist()
        )
    
    print(f"\nVector database built successfully!")
    print(f"Total documents: {collection.count()}")

def verify_database(collection, model, device):
    """Verify database with sample queries"""
    print("\n" + "="*60)
    print("VERIFICATION TEST")
    print("="*60)
    
    test_queries = [
        "How do I reset my password?",
        "My payment failed, what should I do?",
        "I need help with my account"
    ]
    
    for test_query in test_queries:
        print(f"\nTest query: '{test_query}'")
        
        # Embed the query
        query_embedding = model.encode(test_query, convert_to_tensor=False).tolist()
        
        # Search for similar documents
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )
        
        print(f"Top 2 similar results:")
        for i, (metadata, distance) in enumerate(zip(
            results['metadatas'][0],
            results['distances'][0]
        ), 1):
            print(f"  {i}. Similarity: {1 - distance:.4f} | Company: {metadata['company']}")
            print(f"     Q: {metadata['customer_query'][:80]}...")
            print(f"     A: {metadata['support_response'][:80]}...")
    
    print("\n" + "="*60)

def main():
    """Main execution flow"""
    print("="*60)
    print("BUILDING VECTOR DATABASE FOR RAG CHATBOT")
    print("="*60)
    
    if MAX_ROWS:
        print(f"[CONFIG] Dataset limit: {MAX_ROWS:,} rows")
    else:
        print(f"[CONFIG] Using full dataset")
    print(f"[CONFIG] Batch size: {BATCH_SIZE}")
    
    try:
        # Step 0: Check GPU
        device = check_gpu()
        
        # Step 1: Load data
        df = load_data()
        
        # Step 2: Initialize embedding model with GPU
        model = initialize_embedding_model(device)
        
        # Step 3: Initialize ChromaDB
        client, collection = initialize_chromadb()
        
        # Step 4: Build vector database with GPU acceleration
        build_vector_db(df, model, collection, device)
        
        # Step 5: Verify with sample queries
        verify_database(collection, model, device)
        
        print("\n[SUCCESS] Vector database is ready for RAG queries!")
        print(f"Location: {CHROMA_PERSIST_DIR}")
        print(f"Total Q&A pairs indexed: {collection.count()}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to build vector database: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())

