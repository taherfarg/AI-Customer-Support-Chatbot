# 🚀 Quick Start Guide - AI Customer Support Chatbot

## ✅ Prerequisites

1. **Ollama installed and running**
   ```bash
   # Start Ollama
   ollama serve
   
   # In another terminal, pull the model
   ollama pull gpt-oss:20b
   ```

2. **Vector database built** (currently running in background ~30-40 min)
   ```bash
   python build_vector_db.py
   ```

## 🎯 Running the Chatbot

### Option 1: Gradio Web Interface (Recommended)
```bash
python app.py
```
Then open your browser to: `http://localhost:7860`

### Option 2: Command Line Test
```bash
python rag_chatbot.py
```

## 📋 Project Structure

```
AI-Customer-Support-Chatbot/
├── build_vector_db.py         # Build ChromaDB vector database (running now)
├── rag_chatbot.py              # RAG pipeline with LangChain + Ollama
├── app.py                      # Gradio web interface
├── requirements.txt            # Python dependencies
├── setup_verify.py             # Environment verification
├── customer_support_qa_clean.csv  # Cleaned dataset (768K rows)
├── chroma_db/                  # Vector database (being built)
└── .env                        # Configuration (optional)
```

## ⚙️ Configuration

Edit values in your `.env` file or at the top of scripts:

```bash
# Ollama
MODEL_NAME=gpt-oss:20b
OLLAMA_BASE_URL=http://localhost:11434

# Vector DB
CHROMA_PERSIST_DIR=./chroma_db
TOP_K_RESULTS=5

# Embeddings
EMBED_MODEL=all-MiniLM-L6-v2

# Gradio
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=false
```

## 🎮 Usage Examples

### Web Interface
1. Launch: `python app.py`
2. Open browser to `http://localhost:7860`
3. Type your question (e.g., "How do I reset my password?")
4. Get AI-powered answers with source citations!

### Python API
```python
from rag_chatbot import RAGChatbot

# Initialize
chatbot = RAGChatbot()

# Ask a question
result = chatbot.query("How do I reset my password?", return_sources=True)
print(result["answer"])
print(result["sources"])
```

## 🔧 Troubleshooting

### Vector DB Not Built Yet
**Error:** `Vector database is empty!`
**Solution:** Wait for `build_vector_db.py` to complete (~30-40 minutes on CPU)

### Ollama Not Running
**Error:** `Connection refused`
**Solution:** 
```bash
ollama serve
```

### Model Not Found
**Error:** `Model 'gpt-oss:20b' not found`
**Solution:**
```bash
ollama pull gpt-oss:20b
```

### Dependencies Missing
```bash
pip install -r requirements.txt
```

## 📊 Current Status

✅ **Completed:**
- Dependencies installed
- Dataset cleaned (768,837 Q&A pairs)
- RAG pipeline built (LangChain + Ollama)
- Gradio web interface created
- CPU-optimized PyTorch installed

⏳ **In Progress:**
- Vector database building (~30-40 min)

🎯 **Next:** Once vector DB completes, run `python app.py`!

## 🎯 Example Questions to Try

- "How do I reset my password?"
- "My payment failed, what should I do?"
- "I can't log into my account"
- "How do I cancel my subscription?"
- "I need help with a refund"
- "How do I update my billing address?"

## 💡 Tips

1. **Toggle Sources** - Enable "Show Sources" to see which conversations were used
2. **Clear Chat** - Use the clear button to start a fresh conversation
3. **Be Specific** - More detailed questions get better answers
4. **Check Context** - Sources show the company and similar queries used

## 🚀 What's Next?

1. ✅ Wait for vector database to complete
2. ✅ Start Ollama: `ollama serve`
3. ✅ Ensure model is available: `ollama pull gpt-oss:20b`
4. ✅ Launch the app: `python app.py`
5. ✅ Open browser: `http://localhost:7860`
6. ✅ Start chatting!

---

**Need help?** Check `README.md` for detailed documentation.

