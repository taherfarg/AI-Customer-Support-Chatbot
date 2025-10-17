# ❓ Frequently Asked Questions (FAQ)

---

## General Questions

### What is this project?

A production-ready AI customer support chatbot using:
- **RAG (Retrieval-Augmented Generation)** for accurate responses
- **Ollama** for local LLM inference (gpt-oss:20b)
- **ChromaDB** for vector database (768K+ Q&A pairs)
- **Gradio** for web interface
- **Voice capabilities** (text-to-speech)

### Why use RAG instead of fine-tuning?

- ✅ **No training needed** - Works with existing data
- ✅ **Easy updates** - Add new Q&As without retraining
- ✅ **Source citations** - Shows where answers come from
- ✅ **Faster** - No need to fine-tune models
- ✅ **Lower cost** - No expensive training runs

### Is this free to use?

Yes! Uses:
- ✅ Open source libraries (MIT License)
- ✅ Local LLM (Ollama) - no API costs
- ✅ Free embeddings (sentence-transformers)
- ✅ Free vector DB (ChromaDB)

---

## Setup Questions

### How long does setup take?

- **Installation**: 5-10 minutes
- **Vector DB Build**: 30-40 minutes (one-time)
- **Total first-time**: ~45-50 minutes

### What are the system requirements?

**Minimum:**
- Python 3.13+
- 8GB RAM
- 10GB disk space
- CPU (any modern processor)

**Recommended:**
- 16GB+ RAM
- SSD storage
- GPU (optional, for faster embeddings)

### Do I need a GPU?

No! The project runs fine on CPU. GPU is optional for:
- Faster embedding generation
- Larger batch processing

### Can I use a different LLM?

Yes! Edit `config/.env`:
```bash
MODEL_NAME=llama2
# or
MODEL_NAME=mistral
# or any Ollama model
```

---

## Usage Questions

### How do I ask questions?

**Web Interface:**
1. Open http://localhost:7860
2. Type your question
3. Get AI response with sources

**Python API:**
```python
from src import RAGChatbot
chatbot = RAGChatbot()
result = chatbot.query("How do I reset my password?")
```

### How accurate are the responses?

The chatbot uses real customer support conversations (768K+), so responses are based on actual support interactions. Quality depends on:
- Query clarity
- Similar examples in dataset
- Model quality (gpt-oss:20b)

### Can I use my own data?

Yes! Replace `data/customer_support_qa_clean.csv` with your data:

**Format:**
```csv
company,input,response,conversation_id
YourCompany,"Customer question","Your response",abc123
```

Then rebuild:
```bash
python scripts/build_vector_db.py
```

### How many questions can it answer?

Unlimited! The chatbot:
- Retrieves relevant examples from 768K+ Q&As
- Generates responses for any customer support question
- Uses RAG to provide contextual answers

---

## Performance Questions

### Why is the first query slow?

The first query loads:
- Embedding model (~90MB)
- Vector database (~2GB)
- LLM model (~12GB)

**Solution:** Keep the app running for faster subsequent queries.

### How can I make it faster?

```bash
# 1. Reduce retrieved documents
TOP_K_RESULTS=3  # default: 5

# 2. Use smaller model
MODEL_NAME=llama2  # instead of gpt-oss:20b

# 3. Enable GPU
FORCE_CPU=false
```

### Can it handle multiple users?

Yes! Gradio supports concurrent users. For high traffic:
- Deploy with Docker
- Use load balancer
- Scale horizontally

---

## Troubleshooting Questions

### "Vector database not found"

**Solution:**
```bash
python scripts/build_vector_db.py
```
Wait 30-40 minutes for it to complete.

### "Ollama connection refused"

**Solution:**
```bash
# Start Ollama
ollama serve

# In another terminal
ollama pull gpt-oss:20b
```

### "Model not found"

**Solution:**
```bash
ollama pull gpt-oss:20b
```

### "Port 7860 already in use"

**Solution:**
Edit `config/.env`:
```bash
GRADIO_SERVER_PORT=8080
```

### Voice not working on Python 3.13?

**Expected:** Speech-to-text has compatibility issues with Python 3.13 (missing `aifc` module). Text-to-speech still works!

**Workaround:** Use text input or downgrade to Python 3.12 for full voice support.

---

## Customization Questions

### How do I change the port?

Edit `config/.env`:
```bash
GRADIO_SERVER_PORT=8080
```

### How do I change the model?

Edit `config/.env`:
```bash
MODEL_NAME=llama2
```

Then restart: `python app.py`

### Can I customize the UI?

Yes! Edit `app.py`. Gradio is highly customizable:
- Change theme
- Add components
- Modify layout
- Custom CSS

### How do I add authentication?

Add to `app.py`:
```python
demo.launch(
    server_port=GRADIO_PORT,
    auth=("username", "password")
)
```

---

## Deployment Questions

### Can I deploy this to production?

Yes! The project is production-ready with:
- ✅ Docker support
- ✅ Configuration management
- ✅ Logging
- ✅ Error handling
- ✅ Health checks

### How do I deploy with Docker?

```bash
docker-compose up --build
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for details.

### Can I deploy to cloud?

Yes! Supports:
- ✅ AWS (EC2, ECS, Lambda)
- ✅ Azure (Container Instances, App Service)
- ✅ GCP (Cloud Run, Compute Engine)
- ✅ Heroku
- ✅ DigitalOcean

See [DEPLOYMENT.md](DEPLOYMENT.md) for guides.

### What about HTTPS/SSL?

Use a reverse proxy (Nginx, Caddy) or deploy to platform with built-in SSL (Heroku, Cloud Run).

---

## Data & Privacy Questions

### Is my data private?

Yes! Everything runs locally:
- ✅ No external APIs (except Ollama)
- ✅ Data stays on your machine
- ✅ No telemetry or tracking

### Can I use this for sensitive data?

Yes, but ensure:
- Secure server deployment
- Access controls (authentication)
- Regular backups
- Compliance with regulations (GDPR, HIPAA, etc.)

### How is the vector database stored?

In `chroma_db/` directory:
- Persisted to disk
- Can be backed up
- Portable between systems

---

## Development Questions

### How do I contribute?

See [CONTRIBUTING.md](CONTRIBUTING.md):
1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit pull request

### How do I run tests?

```bash
pytest tests/ -v
```

### How do I add new features?

1. Read [API.md](API.md)
2. Create branch: `git checkout -b feature/my-feature`
3. Add code in `src/`
4. Add tests in `tests/`
5. Update docs
6. Submit PR

### Where do I report bugs?

Open an issue on GitHub with:
- Description
- Steps to reproduce
- Error messages
- Environment details

---

## License & Legal Questions

### What license is this under?

MIT License - Free to use, modify, and distribute!

### Can I use this commercially?

Yes! MIT License allows commercial use.

### Do I need to credit the project?

Not required by MIT License, but appreciated!

### Can I sell this?

Yes, MIT License allows commercial use. But consider:
- Contributing back improvements
- Maintaining the open source spirit

---

## Model Questions

### What model does it use?

**Default:** gpt-oss:20b (Ollama)

**Alternatives:**
- llama2 (faster, smaller)
- mistral (balanced)
- codellama (code-focused)
- Any Ollama model

### How do I list available models?

```bash
ollama list
```

### Can I use OpenAI GPT?

Yes! Modify `src/rag_chatbot.py`:
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    openai_api_key="your-key"
)
```

Note: This requires OpenAI API (costs apply).

### Can I use Claude or Gemini?

Yes! LangChain supports multiple providers:
- Claude (Anthropic)
- Gemini (Google)
- Cohere
- Hugging Face

Check LangChain docs for integration.

---

## Voice Questions

### Does voice work on Python 3.13?

**Partial:** Text-to-speech works, speech-to-text doesn't (missing `aifc` module).

### How do I fix voice on Python 3.13?

**Options:**
1. Use Python 3.12 for full voice support
2. Accept text-only input (TTS still works)
3. Wait for `speech_recognition` update

### Can I use other TTS engines?

Yes! Edit `src/voice_utils.py`:
```python
# Use pyttsx3 (offline)
import pyttsx3

engine = pyttsx3.init()
engine.say(text)
engine.runAndWait()
```

---

## Performance Optimization Questions

### How do I speed up embeddings?

```bash
# 1. Enable GPU
FORCE_CPU=false

# 2. Increase batch size
BATCH_SIZE=512

# 3. Use smaller embedding model
EMBED_MODEL=all-MiniLM-L6-v2  # default, fast
```

### How do I reduce memory usage?

```bash
# 1. Use smaller model
MODEL_NAME=llama2

# 2. Reduce context
TOP_K_RESULTS=3

# 3. Limit batch size
BATCH_SIZE=64
```

### How do I handle high traffic?

1. **Horizontal scaling:** Multiple instances + load balancer
2. **Caching:** Cache common queries
3. **Queue system:** Process requests asynchronously
4. **CDN:** Serve static assets

---

## Still Have Questions?

- 📖 Check [README.md](../README.md)
- 📚 Read [API.md](API.md)
- 🚀 See [QUICKSTART.md](QUICKSTART.md)
- 🐛 Open an issue on GitHub
- 💬 Start a discussion
- 📧 Contact maintainers

---

**Questions? Ask away!** 💬

*Last updated: October 2025*

