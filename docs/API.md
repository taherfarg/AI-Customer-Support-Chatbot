# API Documentation

## RAGChatbot

Main chatbot class for RAG-powered customer support.

### Initialization

```python
from src import RAGChatbot

chatbot = RAGChatbot()
```

### Methods

#### `query(question, return_sources=False)`

Query the chatbot with a question.

**Parameters:**
- `question` (str): User's question
- `return_sources` (bool): Whether to return source documents

**Returns:**
- `dict`: Response with 'answer', 'question', and optionally 'sources'

**Example:**
```python
result = chatbot.query("How do I reset my password?", return_sources=True)
print(result["answer"])
print(result["sources"])
```

#### `search_similar(query, k=5)`

Search for similar customer support conversations.

**Parameters:**
- `query` (str): Search query
- `k` (int): Number of results

**Returns:**
- `list`: Similar conversations with metadata

**Example:**
```python
results = chatbot.search_similar("password reset", k=3)
for result in results:
    print(f"{result['company']}: {result['customer_query']}")
```

---

## VoiceHandler

Voice processing utilities for STT and TTS.

### Initialization

```python
from src import VoiceHandler

voice = VoiceHandler()
```

### Methods

#### `text_to_speech(text, lang='en')`

Convert text to speech audio file.

**Parameters:**
- `text` (str): Text to convert
- `lang` (str): Language code (default: 'en')

**Returns:**
- `tuple`: (audio_file_path, error_message)

**Example:**
```python
audio_file, error = voice.text_to_speech("Hello, how can I help?")
if not error:
    print(f"Audio saved to: {audio_file}")
```

#### `speech_to_text(audio_path)`

Convert audio file to text.

**Parameters:**
- `audio_path` (str): Path to audio file

**Returns:**
- `tuple`: (transcribed_text, error_message)

**Example:**
```python
text, error = voice.speech_to_text("recording.wav")
if not error:
    print(f"Transcribed: {text}")
```

---

## Configuration

Settings are managed in `config/settings.py`.

### Environment Variables

```python
from config.settings import *

# Vector Database
print(CHROMA_PERSIST_DIR)  # './chroma_db'
print(TOP_K_RESULTS)       # 5

# Models
print(OLLAMA_MODEL)  # 'gpt-oss:20b'
print(EMBED_MODEL)   # 'all-MiniLM-L6-v2'

# Gradio
print(GRADIO_PORT)   # 7860
```

### Custom Configuration

Create `config/.env` file:
```bash
MODEL_NAME=llama2
TOP_K_RESULTS=10
GRADIO_SERVER_PORT=8080
```

---

## Error Handling

All methods return error information:

```python
result = chatbot.query("test")
if result.get("error"):
    print(f"Error: {result['answer']}")
else:
    print(result["answer"])
```

---

## Examples

### Complete Workflow

```python
from src import RAGChatbot, VoiceHandler

# Initialize
chatbot = RAGChatbot()
voice = VoiceHandler()

# Ask question
result = chatbot.query("How do I cancel my subscription?", return_sources=True)
print(f"Answer: {result['answer']}")

# Generate voice response
audio_file, error = voice.text_to_speech(result['answer'])
if not error:
    print(f"Voice saved to: {audio_file}")

# Show sources
for source in result.get('sources', []):
    print(f"Source {source['rank']}: {source['company']}")
```

### Batch Processing

```python
questions = [
    "How do I reset my password?",
    "My payment failed",
    "I can't log in"
]

for q in questions:
    result = chatbot.query(q)
    print(f"Q: {q}")
    print(f"A: {result['answer']}\n")
```

---

## Performance Tips

1. **Reuse Instances:** Initialize once, query multiple times
2. **Adjust Top-K:** Lower `TOP_K_RESULTS` for faster responses
3. **Batch Similar Queries:** Cache common questions
4. **Monitor Memory:** Large datasets may need optimization

---

## Troubleshooting

### Common Issues

**Import Error:**
```python
# Add src to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
```

**Vector DB Not Found:**
```bash
python scripts/build_vector_db.py
```

**Ollama Not Running:**
```bash
ollama serve
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for API contribution guidelines.

