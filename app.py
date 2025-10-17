"""
Gradio Chat Interface for RAG Customer Support Chatbot
Beautiful, modern UI with chat history, source citations, and voice interaction
"""

import gradio as gr
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rag_chatbot import RAGChatbot
from voice_utils import VoiceHandler

# Load configuration
from config.settings import *

# Configuration is loaded from config.settings

# Initialize chatbot and voice handler (will be done once when app starts)
chatbot_instance = None
voice_handler = None

def initialize_chatbot():
    """Initialize the RAG chatbot"""
    global chatbot_instance, voice_handler
    if chatbot_instance is None:
        try:
            chatbot_instance = RAGChatbot()
            voice_handler = VoiceHandler()
            return True, "[OK] Chatbot initialized successfully!"
        except Exception as e:
            return False, f"[ERROR] Error initializing chatbot: {str(e)}"
    return True, "[OK] Chatbot already initialized"

def format_sources(sources):
    """Format source citations as markdown"""
    if not sources:
        return ""
    
    sources_md = "\n\n---\n### 📚 **Sources (Top Similar Conversations)**\n\n"
    for source in sources:
        sources_md += f"""
**{source['rank']}. Company: {source['company']}** | Similarity: {source['similarity']}
- **Customer Query:** {source['customer_query'][:150]}...
- **Support Response:** {source['support_response'][:150]}...

"""
    return sources_md

def chat_function(message, history, show_sources):
    """
    Process user message and return response
    
    Args:
        message: User's input message
        history: Chat history
        show_sources: Whether to show source citations
        
    Returns:
        Updated chat history
    """
    if not message.strip():
        return history
    
    # Check if chatbot is initialized
    if chatbot_instance is None:
        success, msg = initialize_chatbot()
        if not success:
            history.append((message, f"⚠️ {msg}\n\nPlease ensure:\n1. Vector database is built (`python build_vector_db.py`)\n2. Ollama is running (`ollama serve`)\n3. Model is available (`ollama pull gpt-oss:20b`)"))
            return history
    
    # Get response from chatbot
    try:
        result = chatbot_instance.query(message, return_sources=show_sources)
        
        # Format response
        response = result["answer"]
        
        # Add sources if requested
        if show_sources and "sources" in result:
            response += format_sources(result["sources"])
        
        history.append((message, response))
        
    except Exception as e:
        error_msg = f"[ERROR] Error: {str(e)}\n\nPlease check:\n- Ollama is running\n- Model 'gpt-oss:20b' is available\n- Vector database is built"
        history.append((message, error_msg))
    
    return history

def clear_chat():
    """Clear chat history"""
    return [], None

def process_voice_input(audio, history, show_sources):
    """
    Process voice input from user
    
    Args:
        audio: Audio file path from Gradio
        history: Chat history
        show_sources: Whether to show sources
        
    Returns:
        Updated chat history and audio response
    """
    if audio is None:
        return history, None
    
    # Initialize if needed
    if chatbot_instance is None or voice_handler is None:
        initialize_chatbot()
    
    try:
        # Convert speech to text
        text, error = voice_handler.speech_to_text(audio)
        
        if error:
            history.append(("[Voice Input]", f"[ERROR] {error}"))
            return history, None
        
        if not text:
            history.append(("[Voice Input]", "[ERROR] No speech detected"))
            return history, None
        
        # Add transcribed text to history
        print(f"[VOICE] Transcribed: {text}")
        
        # Get chatbot response
        result = chatbot_instance.query(text, return_sources=show_sources)
        response = result["answer"]
        
        # Add sources if requested
        if show_sources and "sources" in result:
            response += format_sources(result["sources"])
        
        history.append((f"[Voice] {text}", response))
        
        # Generate voice response
        audio_response, tts_error = voice_handler.text_to_speech(result["answer"])
        
        if tts_error:
            print(f"TTS Error: {tts_error}")
            return history, None
        
        return history, audio_response
        
    except Exception as e:
        error_msg = f"[ERROR] Voice processing error: {str(e)}"
        history.append(("[Voice Input]", error_msg))
        return history, None

def generate_voice_response(message):
    """
    Generate voice response for text message
    
    Args:
        message: Text message to convert to speech
        
    Returns:
        Audio file path or None
    """
    if not message or voice_handler is None:
        return None
    
    try:
        audio_file, error = voice_handler.text_to_speech(message)
        if error:
            print(f"TTS Error: {error}")
            return None
        return audio_file
    except Exception as e:
        print(f"Voice generation error: {e}")
        return None

# Create Gradio Interface
with gr.Blocks(
    title="AI Customer Support Chatbot",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="cyan",
    ),
    css="""
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    #chatbot {
        height: 600px !important;
    }
    """
) as demo:
    
    # Header
    gr.Markdown(
        """
        # 🤖 AI Customer Support Chatbot
        ### Powered by RAG (Retrieval-Augmented Generation) + Ollama + ChromaDB
        
        Ask me anything about customer support issues! I'm trained on 768K+ real customer support conversations.
        """
    )
    
    # Status indicator
    status_text = gr.Markdown("**Status:** Initializing...")
    
    # Main chat interface
    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                label="Chat History",
                height=500,
                elem_id="chatbot",
                show_copy_button=True,
                avatar_images=(None, "🤖")
            )
            
            # Text Input Section
            with gr.Row():
                msg = gr.Textbox(
                    label="Type Your Message",
                    placeholder="Type your customer support question here... (e.g., 'How do I reset my password?')",
                    lines=2,
                    scale=4
                )
                send_btn = gr.Button("Send 📤", scale=1, variant="primary")
            
            # Voice Input Section
            gr.Markdown("### Voice Input")
            with gr.Row():
                audio_input = gr.Audio(
                    label="Speak Your Question",
                    sources=["microphone"],
                    type="filepath",
                    scale=3
                )
                voice_btn = gr.Button("Send Voice", scale=1, variant="secondary")
            
            # Voice Output Section
            with gr.Row():
                audio_output = gr.Audio(
                    label="Voice Response",
                    type="filepath",
                    autoplay=False
                )
            
            # Controls
            with gr.Row():
                clear_btn = gr.Button("Clear Chat 🗑️", scale=1)
                show_sources = gr.Checkbox(
                    label="Show Sources",
                    value=True,
                    info="Display similar conversations used to generate the answer",
                    scale=2
                )
                enable_voice_response = gr.Checkbox(
                    label="Voice Responses",
                    value=False,
                    info="Generate voice output for text messages",
                    scale=2
                )
        
        # Sidebar with info
        with gr.Column(scale=1):
            gr.Markdown(
                """
                ### ℹ️ **How to Use**
                
                **Text Mode:**
                1. Type your question
                2. Click "Send 📤" or press Enter
                3. View the AI response
                
                **Voice Mode:**
                1. Click microphone to record
                2. Speak your question
                3. Click "Send Voice"
                4. Get text + voice response
                
                ---
                
                ### 💡 **Example Questions**
                
                - How do I reset my password?
                - My payment failed, what should I do?
                - I can't log into my account
                - How do I cancel my subscription?
                - I need help with a refund
                
                ---
                
                ### ⚙️ **System Info**
                
                - **Model:** gpt-oss:20b (Ollama)
                - **Vector DB:** ChromaDB
                - **Embeddings:** all-MiniLM-L6-v2
                - **Dataset:** 768K+ conversations
                - **Voice:** gTTS + Google STT
                """
            )
    
    # Footer
    gr.Markdown(
        """
        ---
        <center>
        Built with ❤️ using Ollama, LangChain, ChromaDB & Gradio | 
        <a href="https://github.com/" target="_blank">GitHub</a>
        </center>
        """
    )
    
    # Initialize chatbot when app loads
    def on_load():
        success, msg = initialize_chatbot()
        if success:
            return "**Status:** [READY] Ask me anything about customer support."
        else:
            return f"**Status:** ⚠️ {msg}"
    
    # Set up event handlers
    demo.load(on_load, outputs=status_text)
    
    # Text input handlers
    def handle_text_input(message, history, show_sources, enable_voice):
        new_history = chat_function(message, history, show_sources)
        voice_output = None
        
        # Generate voice if enabled and there's a response
        if enable_voice and new_history and len(new_history) > 0:
            last_response = new_history[-1][1]
            # Only generate voice for the answer part (not sources)
            if "---" in last_response:
                answer_only = last_response.split("---")[0].strip()
            else:
                answer_only = last_response
            voice_output = generate_voice_response(answer_only)
        
        return new_history, "", voice_output
    
    msg.submit(
        handle_text_input,
        [msg, chatbot, show_sources, enable_voice_response],
        [chatbot, msg, audio_output]
    )
    
    send_btn.click(
        handle_text_input,
        [msg, chatbot, show_sources, enable_voice_response],
        [chatbot, msg, audio_output]
    )
    
    # Voice input handler
    voice_btn.click(
        process_voice_input,
        [audio_input, chatbot, show_sources],
        [chatbot, audio_output]
    )
    
    # Clear chat handler
    clear_btn.click(clear_chat, None, [chatbot, audio_output])

if __name__ == "__main__":
    print("="*60)
    print("STARTING AI CUSTOMER SUPPORT CHATBOT")
    print("="*60)
    print(f"\n[LAUNCH] Starting Gradio interface on port {GRADIO_PORT}")
    print(f"[CONFIG] Share publicly: {GRADIO_SHARE}")
    print("\n[INIT] Please wait while initializing...")
    print("\nMake sure:")
    print("1. [OK] Vector database is built (python build_vector_db.py)")
    print("2. [OK] Ollama is running (ollama serve)")
    print("3. [OK] Model is available (ollama pull gpt-oss:20b)")
    print("\n" + "="*60 + "\n")
    
    demo.launch(
        server_port=GRADIO_PORT,
        share=GRADIO_SHARE,
        show_error=True
    )

