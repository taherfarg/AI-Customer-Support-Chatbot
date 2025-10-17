# 🤖 AI Customer Support Chatbot

<div align="center">

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Powered by Ollama](https://img.shields.io/badge/Powered%20by-Ollama-blue)](https://ollama.ai)
[![RAG](https://img.shields.io/badge/RAG-Enabled-green)](https://www.langchain.com/)

**Production-ready AI-powered customer support chatbot using RAG, Ollama, ChromaDB, and voice capabilities**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Demo](#-demo) • [Contributing](#-contributing)

</div>

---

## 🌟 Features

### Core Capabilities
- 🧠 **RAG-Powered Responses** - Retrieval-Augmented Generation with 768K+ real customer support conversations
- 💬 **Natural Language Understanding** - Context-aware responses using LangChain + Ollama
- 🔍 **Semantic Search** - ChromaDB vector database for intelligent context retrieval
- 🎤 **Voice Integration** - Text-to-speech output for accessibility
- 📚 **Source Citations** - Shows similar conversations used to generate answers
- 🎨 **Modern UI** - Beautiful Gradio interface with chat history

### Technical Highlights
- ⚡ **Local & Private** - Runs entirely on your machine (no cloud APIs required)
- 🔒 **Secure** - No data leaves your infrastructure
- 🚀 **Fast** - Optimized CPU processing with batch embeddings
- 🔧 **Configurable** - Easy customization via environment variables
- 📊 **Scalable** - Handles 768K+ documents with efficient vector search
- 🐳 **Docker Ready** - Containerized deployment (coming soon)

---

## 📁 Project Structure

```
AI-Customer-Support-Chatbot/
├── 📦 src/                      # Source code
│   ├── __init__.py
│   ├── rag_chatbot.py          # RAG pipeline
│   └── voice_utils.py          # Voice processing
│
├── 🎯 app.py                   # Gradio web interface
│
├── 📜 scripts/                  # Utility scripts
│   ├── build_vector_db.py      # Build ChromaDB
│   └── setup_verify.py         # Environment checker
│
├── ⚙️  config/                  # Configuration
│   ├── settings.py             # Centralized config
│   └── .env.example            # Environment template
│
├── 📚 docs/                     # Documentation
│   ├── QUICKSTART.md
│   ├── VOICE_FEATURES.md
│   ├── API.md
│   └── DEPLOYMENT.md
│
├── 🧪 tests/                    # Test suite
│   └── test_rag.py
│
├── 📊 data/                     # Data files
│   └── customer_support_qa_clean.csv
│
├── 📋 requirements.txt          # Dependencies
├── 🐳 Dockerfile                # Docker configuration
├── 📝 LICENSE                   # MIT License
└── 📖 README.md                 # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- [Ollama](https://ollama.ai) installed and running
- 8GB+ RAM (16GB recommended)
- 10GB+ free disk space

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/AI-Customer-Support-Chatbot.git
cd AI-Customer-Support-Chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp config/.env.example config/.env
# Edit config/.env with your settings

# 4. Start Ollama
ollama serve

# 5. Pull the model
ollama pull gpt-oss:20b

# 6. Build vector database (30-40 minutes)
python scripts/build_vector_db.py

# 7. Launch the chatbot
python app.py
```

### Access the App
Open your browser and navigate to: **http://localhost:7860**

---

## 💡 Usage

### Web Interface
1. Open `http://localhost:7860`
2. Type your question (e.g., "How do I reset my password?")
3. Get AI-powered responses with source citations
4. Enable "Voice Responses" for text-to-speech

### Python API
```python
from src import RAGChatbot

# Initialize chatbot
chatbot = RAGChatbot()

# Ask a question
result = chatbot.query(
    "How do I reset my password?",
    return_sources=True
)

print(result["answer"])
print(result["sources"])
```

### Voice Features
```python
from src import VoiceHandler

# Initialize voice handler
voice = VoiceHandler()

# Text to speech
audio_file, error = voice.text_to_speech("Hello, how can I help you?")
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Dataset Size** | 768,837 Q&A pairs |
| **Companies** | 108 unique |
| **Response Time** | < 2 seconds |
| **Embedding Dimension** | 384 |
| **Retrieval Top-K** | 5 documents |
| **Model** | gpt-oss:20b (Ollama) |

---

## 🎯 Use Cases

- 💼 **Customer Support** - Automated 24/7 support responses
- 📚 **Knowledge Base** - Search through support documentation
- 🎓 **Training** - Help new support agents learn
- ♿ **Accessibility** - Voice output for visually impaired
- 📱 **Multi-Channel** - Deploy on web, mobile, Slack, Discord

---

## 🛠️ Configuration

Edit `config/.env` to customize:

```bash
# Model Settings
MODEL_NAME=gpt-oss:20b              # Ollama model
EMBED_MODEL=all-MiniLM-L6-v2        # Embedding model

# Vector Database
TOP_K_RESULTS=5                      # Results to retrieve
CHROMA_PERSIST_DIR=./chroma_db      # DB location

# Interface
GRADIO_SERVER_PORT=7860             # Web port
VOICE_ENABLED=true                  # Enable voice
```

---

## 📚 Documentation

- [📖 Quick Start Guide](docs/QUICKSTART.md)
- [🎤 Voice Features](docs/VOICE_FEATURES.md)
- [🔧 API Reference](docs/API.md)
- [🚀 Deployment Guide](docs/DEPLOYMENT.md)
- [❓ FAQ](docs/FAQ.md)

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test RAG pipeline
python -m pytest tests/test_rag.py -v

# Test voice features
python src/voice_utils.py
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Taher Farg**
- AI Engineer & Developer
- Focus: AI | NLP | Computer Vision | Data Science
- Blog: [onlineumrah1.blogspot.com](https://onlineumrah1.blogspot.com)
- GitHub: [@TaherFarg](https://github.com/TaherFarg)

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Local LLM inference
- [LangChain](https://www.langchain.com) - RAG framework
- [ChromaDB](https://www.trychroma.com) - Vector database
- [Gradio](https://gradio.app) - Web interface
- [Sentence Transformers](https://www.sbert.net) - Embeddings

---

## 📞 Support

- 📧 Email: [your-email@example.com](mailto:your-email@example.com)
- 💬 Issues: [GitHub Issues](https://github.com/yourusername/AI-Customer-Support-Chatbot/issues)
- 📖 Docs: [Documentation](docs/)

---

## 🔮 Roadmap

- [ ] Docker deployment
- [ ] Multi-language support
- [ ] Fine-tuning capabilities
- [ ] Analytics dashboard
- [ ] Slack/Discord integration
- [ ] OpenAI Whisper STT
- [ ] Cloud deployment guides

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Built with ❤️ using Ollama, LangChain, ChromaDB & Gradio

[Report Bug](https://github.com/yourusername/AI-Customer-Support-Chatbot/issues) • [Request Feature](https://github.com/yourusername/AI-Customer-Support-Chatbot/issues)

</div>
