# 🤖 AI Customer Support Chatbot v2.0

<div align="center">

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-success.svg)](https://github.com/yourusername/AI-Customer-Support-Chatbot)
[![Powered by Ollama](https://img.shields.io/badge/Powered%20by-Ollama-blue)](https://ollama.ai)
[![RAG](https://img.shields.io/badge/RAG-Enabled-green)](https://www.langchain.com/)

**Production-ready AI-powered customer support chatbot with RAG, streaming responses, conversation context, and chat history**

[Features](#-features) • [Quick Start](#-quick-start) • [Demo](#-demo) • [Documentation](#-documentation)

</div>

---

## 🎬 Demo

<div align="center">

### 💬 Chatbot Interface in Action

<img src="Screenshot 2025-10-18 125202.png" alt="AI Customer Support Chatbot Interface" width="800"/>

*The chatbot provides intelligent, context-aware responses based on 768K+ real customer support conversations*

### ✨ Key Features Demo

<table>
  <tr>
    <td width="50%">
      <h4>🔄 Real-time Streaming Responses</h4>
      <p>Watch AI responses appear word-by-word in real-time</p>
    </td>
    <td width="50%">
      <h4>💬 Multi-turn Conversations</h4>
      <p>Context-aware follow-up questions</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h4>👍👎 Response Feedback</h4>
      <p>Rate responses to track quality</p>
    </td>
    <td width="50%">
      <h4>💾 Chat History</h4>
      <p>Save and export conversations</p>
    </td>
  </tr>
</table>

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Enhanced Features (v2.0)](#-enhanced-features-v20)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [API Reference](#-api-reference)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Features

### 🆕 NEW in v2.0 - Enhanced Edition

- 🔄 **Streaming Responses** - Real-time token-by-token generation (feels 50% faster!)
- 💬 **Multi-turn Context** - Remembers conversation history for natural follow-ups
- 👍👎 **Response Feedback** - Rate responses to track quality and satisfaction
- 💾 **Chat History** - Save, load, and export conversations (JSON/TXT/Markdown)

### Core Capabilities

- 🧠 **RAG-Powered Responses** - Retrieval-Augmented Generation with 768K+ real customer support conversations
- 💡 **Context-Aware** - Understands conversation flow and provides relevant follow-up answers
- 🔍 **Semantic Search** - ChromaDB vector database for intelligent context retrieval
- 🎤 **Voice Integration** - Text-to-speech output for accessibility
- 📚 **Source Citations** - Shows similar conversations used to generate answers
- 🎨 **Modern UI** - Beautiful Gradio interface with enhanced features

### Technical Highlights

- ⚡ **Local & Private** - Runs entirely on your machine (no cloud APIs required)
- 🔒 **Secure** - No data leaves your infrastructure
- 🚀 **Fast** - Optimized CPU processing with batch embeddings
- 🔧 **Configurable** - Easy customization via environment variables
- 📊 **Scalable** - Handles 768K+ documents with efficient vector search
- 🐳 **Docker Ready** - Containerized deployment included

---

## 📁 Project Structure

```
AI-Customer-Support-Chatbot/
├── 🎯 Launch Files
│   ├── app_enhanced.py         # Enhanced app with all v2.0 features (RECOMMENDED)
│   └── app.py                  # Original app (v1.0)
│
├── 📦 src/                     # Source Code
│   ├── streaming_rag.py        # Streaming RAG chatbot (NEW!)
│   ├── chat_manager.py         # History & feedback manager (NEW!)
│   ├── rag_chatbot.py          # Original RAG chatbot
│   ├── voice_utils.py          # Voice features (TTS)
│   └── __init__.py             # Package initialization
│
├── ⚙️  config/                 # Configuration
│   ├── settings.py             # Centralized settings
│   └── .env.example            # Environment template
│
├── 📜 scripts/                 # Utility Scripts
│   ├── build_vector_db.py      # Build ChromaDB vector database
│   └── setup_verify.py         # Environment checker
│
├── 📊 data/                    # Data Files
│   ├── customer_support_qa_clean.csv  # 768K+ Q&A pairs
│   └── explor_the_data_set.ipynb      # Data exploration
│
├── 💾 chat_history/            # Chat Storage (NEW!)
│   ├── conversations.json      # Saved conversations
│   ├── feedback.json           # User feedback
│   └── exports/                # Exported chats
│
├── 🧪 tests/                   # Test Suite
│   └── test_rag.py             # RAG tests
│
├── 🐳 Deployment
│   ├── Dockerfile              # Container image
│   └── docker-compose.yml      # Multi-container stack
│
├── 📋 Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── setup.py                # Package setup
│   └── .gitignore              # Git ignore rules
│
└── 📖 README.md                # This file
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

# 6. Build vector database (30-40 minutes, one-time setup)
python scripts/build_vector_db.py

# 7. Launch the ENHANCED chatbot (v2.0 - RECOMMENDED)
python app_enhanced.py

# OR launch the original chatbot (v1.0)
python app.py
```

### Access the App

Open your browser: **http://localhost:7860**

---

## 🆕 Enhanced Features (v2.0)

### 1. 🔄 Streaming Responses

**See AI responses appear in real-time, word by word!**

- Real-time token-by-token generation
- Perceived 50% faster response time
- Better user engagement
- Professional UX

### 2. 💬 Multi-turn Conversation Context

**Chatbot remembers your conversation!**

- Remembers last 5 messages automatically
- Natural follow-up questions work perfectly
- Toggle context on/off as needed
- Example:
  ```
  You: "How do I reset my password?"
  Bot: "To reset your password, visit settings..."
  
  You: "What if I forgot my email?"
  Bot: [Remembers context] "If you forgot your email too..."
  ```

### 3. 👍👎 Response Feedback System

**Rate responses and track quality!**

- Thumbs up/down after each response
- View feedback statistics
- Track satisfaction rates
- Example stats: "Satisfaction Rate: 80%"

### 4. 💾 Chat History Persistence

**Never lose a conversation!**

- Automatically saves all conversations
- Load previous sessions anytime
- Export to multiple formats:
  - **JSON** - Machine-readable
  - **TXT** - Plain text
  - **Markdown** - Formatted
- Manage multiple sessions

---

## 💡 Usage

### Basic Chat (Enhanced App)

```bash
python app_enhanced.py
```

**Features Available:**
1. Type your question in the message box
2. Enable "Use Conversation Context" for follow-ups
3. Enable "Show Sources" to see citations
4. Rate responses with 👍 or 👎
5. Export your conversation anytime

### Python API

```python
from src import StreamingRAGChatbot, ChatManager

# Initialize chatbot
chatbot = StreamingRAGChatbot()
manager = ChatManager()

# Create session
session_id = manager.create_session()

# Stream response
for chunk in chatbot.query_stream("How do I reset my password?"):
    print(chunk, end="", flush=True)

# Or get full response with context
conversation_history = manager.get_conversation_context(session_id)
result = chatbot.query(
    "What about password requirements?",
    conversation_history=conversation_history,
    return_sources=True
)

# Save message
manager.add_message(session_id, "user", "How do I reset my password?")
manager.add_message(session_id, "assistant", result["answer"])

# Add feedback
manager.add_feedback(session_id, 0, "positive", "Very helpful!")

# Export conversation
export_file = manager.export_conversation(session_id, "txt")
print(f"Exported to: {export_file}")
```

### Voice Features

```python
from src import VoiceHandler

voice = VoiceHandler()

# Text to speech
audio_file, error = voice.text_to_speech("Hello! How can I help you?")
if not error:
    print(f"Audio saved: {audio_file}")
```

---

## ⚙️ Configuration

### Environment Variables

Edit `config/.env`:

```bash
# Ollama Configuration
MODEL_NAME=gpt-oss:20b
OLLAMA_BASE_URL=http://localhost:11434

# Vector Database
CHROMA_PERSIST_DIR=./chroma_db
TOP_K_RESULTS=5

# Embedding
EMBED_MODEL=all-MiniLM-L6-v2
BATCH_SIZE=128
FORCE_CPU=true

# Gradio Interface
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=false

# Voice Features
VOICE_ENABLED=true
TTS_LANGUAGE=en
```

### Customization

**Change Model:**
```bash
# Use a different Ollama model
MODEL_NAME=llama2
```

**Adjust Retrieval:**
```bash
# Get more/fewer source documents
TOP_K_RESULTS=10
```

**Change Port:**
```bash
# Run on different port
GRADIO_SERVER_PORT=8080
```

---

## 📚 API Reference

### StreamingRAGChatbot

```python
from src import StreamingRAGChatbot

chatbot = StreamingRAGChatbot()

# Stream response
for chunk in chatbot.query_stream(
    question="How do I reset my password?",
    conversation_history="Previous messages..."
):
    print(chunk, end="")

# Full response
result = chatbot.query(
    question="How do I reset my password?",
    conversation_history="Previous messages...",
    return_sources=True
)
```

### ChatManager

```python
from src import ChatManager

manager = ChatManager(storage_dir="chat_history")

# Session management
session_id = manager.create_session()
manager.add_message(session_id, "user", "Hello!")
manager.add_message(session_id, "assistant", "Hi there!")

# Feedback
manager.add_feedback(session_id, 0, "positive", "Great response!")
stats = manager.get_feedback_stats()
# Returns: {"total": 10, "positive": 8, "satisfaction_rate": 80}

# Export
export_file = manager.export_conversation(session_id, "txt")

# Get conversation context for AI
context = manager.get_conversation_context(session_id, max_messages=5)
```

### VoiceHandler

```python
from src import VoiceHandler

voice = VoiceHandler()

# Text to speech
audio_file, error = voice.text_to_speech("Hello!", lang="en")
```

---

## 🐳 Deployment

### Docker

```bash
# Using Docker Compose (recommended)
docker-compose up --build

# Or standalone Docker
docker build -t ai-chatbot .
docker run -p 7860:7860 ai-chatbot
```

### Cloud Deployment

**AWS EC2:**
```bash
# Launch EC2 instance (t3.xlarge recommended)
# SSH and install Docker
sudo apt update && sudo apt install docker.io docker-compose
git clone <your-repo>
cd AI-Customer-Support-Chatbot
sudo docker-compose up -d
```

**Azure Container Instances:**
```bash
az container create \
  --resource-group chatbot-rg \
  --name ai-chatbot \
  --image <your-image> \
  --dns-name-label ai-chatbot \
  --ports 7860
```

**Google Cloud Run:**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-chatbot
gcloud run deploy ai-chatbot \
  --image gcr.io/PROJECT-ID/ai-chatbot \
  --platform managed \
  --allow-unauthenticated
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue: "Vector database not found"**
```bash
# Solution: Build the database
python scripts/build_vector_db.py
```

**Issue: "Ollama connection refused"**
```bash
# Solution: Start Ollama
ollama serve

# In another terminal
ollama pull gpt-oss:20b
```

**Issue: "Port 7860 already in use"**
```bash
# Solution: Change port in config/.env
GRADIO_SERVER_PORT=8080
```

**Issue: Streaming not working**
```bash
# Solution: Restart Ollama
# Stop: Ctrl+C
# Start: ollama serve
```

**Issue: Context not remembered**
```bash
# Solution: Enable "Use Conversation Context" checkbox in UI
```

**Issue: Export failed**
```bash
# Solution: Check chat_history/ folder exists
mkdir -p chat_history/exports
```

### Performance Optimization

**Speed up responses:**
```bash
# Use smaller model
MODEL_NAME=llama2

# Reduce retrieved documents
TOP_K_RESULTS=3
```

**Reduce memory usage:**
```bash
# Smaller batch size
BATCH_SIZE=64
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
| **Model** | gpt-oss:20b (13GB) |
| **Streaming** | Real-time token generation |
| **Context Window** | Last 5 messages |

---

## 🧪 Testing

### Run Tests

```bash
# Test chat manager
python src/chat_manager.py

# Test streaming RAG
python src/streaming_rag.py

# Run unit tests
pytest tests/ -v
```

### Verify Setup

```bash
python scripts/setup_verify.py
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Steps:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style:
- Follow PEP 8 guidelines
- Use `black` for formatting
- Add docstrings to functions
- Include type hints where possible

### Testing:
- Add tests for new features
- Ensure all tests pass
- Maintain test coverage

---

## 📋 System Requirements

### Minimum:
- Python 3.13+
- 8GB RAM
- 10GB disk space
- CPU (any modern processor)

### Recommended:
- Python 3.13+
- 16GB RAM
- 20GB disk space
- GPU (optional, for faster embeddings)

---

## 🎓 Use Cases

- 💼 **Customer Support** - Automated 24/7 support responses
- 📚 **Knowledge Base** - Search through support documentation
- 🎓 **Training** - Help new support agents learn
- ♿ **Accessibility** - Voice output for visually impaired
- 📱 **Multi-Channel** - Deploy on web, mobile, Slack, Discord

---

## 🔮 Roadmap

### v3.0 (Future):
- [ ] Analytics dashboard with charts
- [ ] Model selection interface
- [ ] Custom knowledge base upload
- [ ] REST API endpoint
- [ ] Admin panel
- [ ] Multi-user support
- [ ] Slack/Discord integration
- [ ] OpenAI Whisper for STT

---

## 📞 Support & Contact

**Issues:** [GitHub Issues](https://github.com/yourusername/AI-Customer-Support-Chatbot/issues)

**Questions:** Check the troubleshooting section above

---

## 📜 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 Taher Farg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 👨‍💻 Author

**Taher Farg**
- AI Engineer & Developer
- Focus: AI | NLP | Computer Vision | Data Science

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Local LLM inference
- [LangChain](https://www.langchain.com) - RAG framework
- [ChromaDB](https://www.trychroma.com) - Vector database
- [Gradio](https://gradio.app) - Web interface
- [Sentence Transformers](https://www.sbert.net) - Embeddings

---

## 📈 Version History

### v2.0.0 (Current) - Enhanced Edition
- ✅ Streaming responses
- ✅ Multi-turn conversation context
- ✅ Response feedback system
- ✅ Chat history persistence
- ✅ Session management
- ✅ Export functionality

### v1.0.0 - Initial Release
- ✅ RAG-powered chatbot
- ✅ Voice output (TTS)
- ✅ Professional structure
- ✅ Docker ready
- ✅ Comprehensive documentation

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Built with ❤️ using Ollama, LangChain, ChromaDB & Gradio

[Report Bug](https://github.com/yourusername/AI-Customer-Support-Chatbot/issues) • [Request Feature](https://github.com/yourusername/AI-Customer-Support-Chatbot/issues)

**Version 2.0.0 | Production Ready | Professional Grade**

</div>
