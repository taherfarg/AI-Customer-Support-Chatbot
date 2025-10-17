# 🚀 Getting Started - Professional Edition

Welcome to your **professional-grade AI Customer Support Chatbot**!

---

## 📖 Quick Navigation

| Document | Purpose |
|----------|---------|
| **This File** | Getting started guide |
| [README.md](README.md) | Main documentation |
| [QUICKSTART.md](docs/QUICKSTART.md) | Fast setup |
| [API.md](docs/API.md) | API reference |
| [PROFESSIONAL_UPGRADE.md](PROFESSIONAL_UPGRADE.md) | What changed |

---

## ✅ Prerequisites Check

Run the verification script:
```bash
python scripts/setup_verify.py
```

**Expected Output:**
```
✅ Dependencies installed
✅ Data file found
✅ Ollama running
✅ Model available
```

---

## 🎯 3-Step Quick Start

### Step 1: Ensure Vector Database is Built

If not already built:
```bash
python scripts/build_vector_db.py
```

⏱️ **Time**: ~30-40 minutes (one-time setup)
📊 **Result**: 768K+ embeddings in ChromaDB

### Step 2: Start Ollama (if not running)

```bash
ollama serve
```

Leave this running in a separate terminal.

### Step 3: Launch the Chatbot

```bash
python app.py
```

🌐 **Access**: http://localhost:7860

---

## 🎨 Using the Chatbot

### Web Interface
1. Open browser to `http://localhost:7860`
2. Type a question (e.g., "How do I reset my password?")
3. Get AI-powered responses with sources
4. Enable "Voice Responses" for audio output

### Features
- 💬 Chat with message history
- 📚 Source citations from real support conversations
- 🎤 Voice responses (text-to-speech)
- 🔄 Real-time responses
- 📊 Performance metrics

---

## ⚙️ Configuration

Edit `config/.env` to customize:

```bash
# Change the model
MODEL_NAME=llama2

# Adjust response quality
TOP_K_RESULTS=10

# Change port
GRADIO_SERVER_PORT=8080

# Enable GPU for embeddings
FORCE_CPU=false
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Easiest)

```bash
docker-compose up --build
```

This starts both the chatbot and Ollama server.

### Using Docker Alone

```bash
# Build
docker build -t ai-chatbot .

# Run
docker run -p 7860:7860 \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/data:/app/data \
  ai-chatbot
```

---

## 🧪 Testing

### Run Setup Verification
```bash
python scripts/setup_verify.py
```

### Run Unit Tests
```bash
pytest tests/ -v
```

### Test RAG Pipeline
```python
from src import RAGChatbot

chatbot = RAGChatbot()
result = chatbot.query("How do I reset my password?")
print(result["answer"])
```

### Test Voice Features
```python
from src import VoiceHandler

voice = VoiceHandler()
audio, error = voice.text_to_speech("Hello!")
print(f"Audio saved: {audio}")
```

---

## 📚 Python API Usage

### Basic Query
```python
from src import RAGChatbot

# Initialize
chatbot = RAGChatbot()

# Ask a question
result = chatbot.query("How do I cancel my subscription?")

# Get the answer
print(result["answer"])
```

### Query with Sources
```python
result = chatbot.query(
    "My payment failed",
    return_sources=True
)

print(result["answer"])
print(f"Used {len(result['sources'])} sources")
```

### Voice Integration
```python
from src import VoiceHandler

voice = VoiceHandler()

# Get chatbot response
result = chatbot.query("Help me")

# Convert to speech
audio_file, error = voice.text_to_speech(result["answer"])
print(f"Play: {audio_file}")
```

---

## 📁 Project Structure

```
AI-Customer-Support-Chatbot/
├── app.py                 # 🎯 Start here! Web interface
├── src/                   # Source code
│   ├── rag_chatbot.py    # RAG pipeline
│   └── voice_utils.py    # Voice processing
├── scripts/              # Utilities
│   ├── build_vector_db.py # Build database
│   └── setup_verify.py   # Check setup
├── config/               # Configuration
│   ├── settings.py       # Settings
│   └── .env              # Environment
├── docs/                 # Documentation
├── tests/                # Test suite
└── data/                 # Data files
```

---

## 🔧 Troubleshooting

### Issue: "Vector database not found"
**Solution:**
```bash
python scripts/build_vector_db.py
```

### Issue: "Ollama connection refused"
**Solution:**
```bash
ollama serve
```
Leave it running, then restart the chatbot.

### Issue: "Model not found"
**Solution:**
```bash
ollama pull gpt-oss:20b
```

### Issue: Import errors
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Port 7860 already in use"
**Solution:**
Edit `config/.env`:
```bash
GRADIO_SERVER_PORT=8080
```

---

## 💡 Usage Examples

### Customer Support
```python
chatbot.query("I can't log into my account")
chatbot.query("How do I change my email address?")
chatbot.query("My payment was declined")
```

### Search Similar Issues
```python
similar = chatbot.search_similar("password reset", k=5)
for item in similar:
    print(f"{item['company']}: {item['customer_query']}")
```

### Custom Configuration
```python
from src import RAGChatbot

chatbot = RAGChatbot(
    model_name="llama2",
    top_k=10
)
```

---

## 🎓 Learn More

### Documentation
- 📖 [README.md](README.md) - Full documentation
- 🚀 [QUICKSTART.md](docs/QUICKSTART.md) - Fast setup
- 📚 [API.md](docs/API.md) - API reference
- 🤝 [CONTRIBUTING.md](docs/CONTRIBUTING.md) - Contribute

### Guides
- 🎤 [VOICE_FEATURES.md](docs/VOICE_FEATURES.md) - Voice capabilities
- 🏗️ [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - Structure explanation
- ⬆️ [PROFESSIONAL_UPGRADE.md](PROFESSIONAL_UPGRADE.md) - What's new

---

## 🚀 Next Steps

### For Development:
1. ✅ Read [API.md](docs/API.md)
2. ✅ Check [CONTRIBUTING.md](docs/CONTRIBUTING.md)
3. ✅ Run tests: `pytest tests/`
4. ✅ Extend features

### For Deployment:
1. ✅ Try Docker: `docker-compose up`
2. ✅ Configure production settings
3. ✅ Set up monitoring
4. ✅ Deploy to cloud

### For Collaboration:
1. ✅ Push to GitHub
2. ✅ Add CI/CD
3. ✅ Invite contributors
4. ✅ Build community

---

## 📞 Support

- 📖 Documentation: See `docs/` folder
- 🐛 Issues: GitHub Issues
- 💬 Questions: Open a discussion
- 📧 Contact: See README

---

## 🎉 You're Ready!

**Your professional AI chatbot is ready to use!**

### Start Now:
```bash
# 1. Verify setup
python scripts/setup_verify.py

# 2. Launch chatbot
python app.py

# 3. Open browser
# http://localhost:7860
```

---

**Built with ❤️ using Ollama, LangChain, ChromaDB & Gradio**

*Professional Edition - October 2025*

