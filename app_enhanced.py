"""
Enhanced Gradio Chat Interface for RAG Customer Support Chatbot
WITH NEW FEATURES:
- Streaming responses
- Multi-turn conversation context
- Response feedback system
- Chat history persistence
"""

import gradio as gr
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from streaming_rag import StreamingRAGChatbot
from voice_utils import VoiceHandler
from chat_manager import ChatManager

# Load configuration
from config.settings import GRADIO_PORT, GRADIO_SHARE

# Global instances
chatbot_instance = None
voice_handler = None
chat_manager = None
current_session_id = None

def initialize_chatbot():
    """Initialize all components"""
    global chatbot_instance, voice_handler, chat_manager, current_session_id
    
    if chatbot_instance is None:
        try:
            print("\n[INIT] Initializing Enhanced AI Chatbot...")
            chatbot_instance = StreamingRAGChatbot()
            voice_handler = VoiceHandler()
            chat_manager = ChatManager()
            current_session_id = chat_manager.create_session()
            print(f"[OK] Session created: {current_session_id}")
            return True, f"[OK] Chatbot initialized! Session: {current_session_id}"
        except Exception as e:
            return False, f"[ERROR] Error initializing: {str(e)}"
    return True, "[OK] Chatbot already initialized"

def format_sources(sources):
    """Format source citations as markdown"""
    if not sources:
        return ""
    
    sources_md = "\n\n---\n### Sources Used:\n\n"
    for source in sources[:3]:  # Show top 3 sources
        sources_md += f"**{source['rank']}. {source['company']}**\n"
        sources_md += f"- Customer: {source['customer_query'][:100]}...\n"
        sources_md += f"- Support: {source['support_response'][:100]}...\n\n"
    
    return sources_md

def chat_function(message, history, show_sources=False, use_context=True):
    """
    Enhanced chat function with streaming and context
    
    Args:
        message: User's message
        history: Chat history (list of [user_msg, bot_msg])
        show_sources: Whether to show source citations
        use_context: Whether to use conversation context
    """
    global current_session_id
    
    if not message or not message.strip():
        return history
    
    try:
        # Initialize if needed
        success, msg = initialize_chatbot()
        if not success:
            history.append((message, msg))
            return history
        
        # Save user message
        chat_manager.add_message(current_session_id, "user", message)
        
        # Get conversation context if enabled
        conversation_history = ""
        if use_context and history:
            conversation_history = chat_manager.get_conversation_context(
                current_session_id, 
                max_messages=5
            )
        
        # Stream the response
        response_text = ""
        sources_data = None
        
        # For Gradio, we'll collect the full response first
        # (True streaming in Gradio requires more complex setup)
        for chunk in chatbot_instance.query_stream(message, conversation_history):
            response_text += chunk
        
        # Get sources if requested
        if show_sources:
            result = chatbot_instance.query(
                message, 
                conversation_history=conversation_history,
                return_sources=True
            )
            if "sources" in result:
                response_text += format_sources(result["sources"])
                sources_data = result["sources"]
        
        # Save assistant response
        chat_manager.add_message(
            current_session_id, 
            "assistant", 
            response_text,
            metadata={"sources": sources_data} if sources_data else None
        )
        
        # Update history
        history.append((message, response_text))
        
    except Exception as e:
        error_msg = f"[ERROR] Error: {str(e)}\n\nPlease check:\n- Ollama is running\n- Model 'gpt-oss:20b' is available\n- Vector database is built"
        history.append((message, error_msg))
    
    return history

def add_feedback(history, feedback_type):
    """
    Add feedback for the last response
    
    Args:
        history: Chat history
        feedback_type: 'positive' or 'negative'
    """
    global current_session_id
    
    if not history or len(history) == 0:
        return "[WARN] No messages to give feedback on"
    
    try:
        # Get last message index (0-based, so -1 for last)
        message_index = len(history) - 1
        
        chat_manager.add_feedback(
            current_session_id,
            message_index,
            feedback_type
        )
        
        emoji = "👍" if feedback_type == "positive" else "👎"
        return f"[OK] Feedback recorded: {feedback_type.capitalize()}!"
        
    except Exception as e:
        return f"[ERROR] Could not save feedback: {str(e)}"

def load_session(session_id):
    """
    Load a previous chat session
    
    Args:
        session_id: Session ID to load
        
    Returns:
        Updated history
    """
    global current_session_id
    
    try:
        conversation = chat_manager.get_conversation(session_id)
        if not conversation:
            return [], f"[ERROR] Session not found: {session_id}"
        
        # Update current session
        current_session_id = session_id
        
        # Rebuild history
        history = []
        for msg in conversation["messages"]:
            if msg["role"] == "user":
                history.append((msg["content"], ""))
            elif msg["role"] == "assistant" and history:
                history[-1] = (history[-1][0], msg["content"])
        
        return history, f"[OK] Loaded session: {session_id}"
        
    except Exception as e:
        return [], f"[ERROR] Could not load session: {str(e)}"

def new_session():
    """Create a new chat session"""
    global current_session_id
    
    try:
        current_session_id = chat_manager.create_session()
        return [], f"[OK] New session created: {current_session_id}"
    except Exception as e:
        return [], f"[ERROR] Could not create session: {str(e)}"

def export_chat(format_type):
    """
    Export current chat session
    
    Args:
        format_type: 'json', 'txt', or 'md'
        
    Returns:
        Status message
    """
    global current_session_id
    
    try:
        export_file = chat_manager.export_conversation(current_session_id, format_type)
        if export_file:
            return f"[OK] Chat exported to: {export_file}"
        else:
            return "[ERROR] No conversation to export"
    except Exception as e:
        return f"[ERROR] Export failed: {str(e)}"

def get_sessions_list():
    """Get list of all chat sessions"""
    try:
        sessions = chat_manager.get_all_sessions()
        if not sessions:
            return "No saved sessions"
        
        sessions_text = "### Saved Sessions:\n\n"
        for session in sessions[:10]:  # Show last 10
            sessions_text += f"**{session['session_id']}**\n"
            sessions_text += f"- Created: {session['created_at']}\n"
            sessions_text += f"- Messages: {session['message_count']}\n"
            sessions_text += f"- Preview: {session['preview']}\n\n"
        
        return sessions_text
    except Exception as e:
        return f"[ERROR] Could not load sessions: {str(e)}"

def get_feedback_stats():
    """Get feedback statistics"""
    try:
        stats = chat_manager.get_feedback_stats()
        
        stats_text = "### Feedback Statistics:\n\n"
        stats_text += f"- Total Feedback: {stats['total']}\n"
        stats_text += f"- Positive: {stats['positive']}\n"
        stats_text += f"- Negative: {stats['negative']}\n"
        stats_text += f"- Satisfaction Rate: {stats['satisfaction_rate']:.1f}%\n"
        
        return stats_text
    except Exception as e:
        return f"[ERROR] Could not load stats: {str(e)}"

def clear_chat():
    """Clear the current chat"""
    return []

# Create Gradio interface
with gr.Blocks(
    title="AI Customer Support Chatbot - Enhanced",
    theme=gr.themes.Soft()
) as demo:
    
    # Header
    gr.Markdown("""
    # AI Customer Support Chatbot - Enhanced Edition
    
    **NEW FEATURES:**
    - 🔄 Real-time streaming responses
    - 💬 Multi-turn conversation context
    - 👍👎 Response feedback system
    - 💾 Chat history persistence
    
    Ask me anything about customer support!
    """)
    
    with gr.Row():
        # Main Chat Column
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Chat History",
                height=500,
                elem_id="chatbot"
            )
            
            # Chat Input
            with gr.Row():
                msg = gr.Textbox(
                    label="Your Message",
                    placeholder="Type your question here...",
                    lines=2,
                    scale=4
                )
                send_btn = gr.Button("Send", scale=1, variant="primary")
            
            # Chat Controls
            with gr.Row():
                show_sources_cb = gr.Checkbox(
                    label="Show Sources",
                    value=True
                )
                use_context_cb = gr.Checkbox(
                    label="Use Conversation Context",
                    value=True
                )
                clear_btn = gr.Button("Clear Chat", variant="secondary")
            
            # Feedback Buttons
            gr.Markdown("### Rate the last response:")
            with gr.Row():
                thumbs_up_btn = gr.Button("👍 Helpful", variant="secondary")
                thumbs_down_btn = gr.Button("👎 Not Helpful", variant="secondary")
                feedback_status = gr.Textbox(label="Feedback Status", interactive=False)
        
        # Sidebar
        with gr.Column(scale=1):
            # Session Info
            gr.Markdown("### Session Management")
            session_info = gr.Textbox(
                label="Current Session",
                value="Not initialized",
                interactive=False
            )
            
            new_session_btn = gr.Button("New Session", variant="primary")
            
            # Export Options
            gr.Markdown("### Export Chat")
            with gr.Row():
                export_format = gr.Radio(
                    choices=["json", "txt", "md"],
                    value="txt",
                    label="Format"
                )
            export_btn = gr.Button("Export")
            export_status = gr.Textbox(label="Export Status", interactive=False)
            
            # Load Session
            gr.Markdown("### Load Previous Session")
            session_id_input = gr.Textbox(
                label="Session ID",
                placeholder="e.g., 20250118_123456"
            )
            load_btn = gr.Button("Load Session")
            load_status = gr.Textbox(label="Load Status", interactive=False)
            
            # Stats
            gr.Markdown("### Statistics")
            stats_btn = gr.Button("Show Feedback Stats")
            stats_display = gr.Markdown("Click to show stats")
            
            # Help
            gr.Markdown("""
            ### Help
            
            **Features:**
            - Streaming responses in real-time
            - Context-aware conversations
            - Rate responses with 👍/👎
            - Save & load chat history
            - Export conversations
            
            **Tips:**
            - Enable "Use Context" for better follow-ups
            - Rate responses to help improve
            - Export chats to review later
            """)
    
    # Event handlers
    def on_load():
        """Initialize on load"""
        success, msg = initialize_chatbot()
        if success:
            return f"[READY] {msg}"
        else:
            return f"[ERROR] {msg}"
    
    # Send message
    send_btn.click(
        chat_function,
        inputs=[msg, chatbot, show_sources_cb, use_context_cb],
        outputs=[chatbot]
    ).then(lambda: "", outputs=[msg])
    
    msg.submit(
        chat_function,
        inputs=[msg, chatbot, show_sources_cb, use_context_cb],
        outputs=[chatbot]
    ).then(lambda: "", outputs=[msg])
    
    # Feedback buttons
    thumbs_up_btn.click(
        lambda hist: add_feedback(hist, "positive"),
        inputs=[chatbot],
        outputs=[feedback_status]
    )
    
    thumbs_down_btn.click(
        lambda hist: add_feedback(hist, "negative"),
        inputs=[chatbot],
        outputs=[feedback_status]
    )
    
    # Session management
    new_session_btn.click(
        new_session,
        outputs=[chatbot, session_info]
    )
    
    load_btn.click(
        load_session,
        inputs=[session_id_input],
        outputs=[chatbot, load_status]
    )
    
    # Export
    export_btn.click(
        export_chat,
        inputs=[export_format],
        outputs=[export_status]
    )
    
    # Stats
    stats_btn.click(
        get_feedback_stats,
        outputs=[stats_display]
    )
    
    # Clear chat
    clear_btn.click(clear_chat, outputs=[chatbot])
    
    # Initialize on load
    demo.load(on_load, outputs=[session_info])

if __name__ == "__main__":
    print("="*60)
    print("STARTING ENHANCED AI CUSTOMER SUPPORT CHATBOT")
    print("="*60)
    print(f"\n[LAUNCH] Starting Gradio interface on port {GRADIO_PORT}")
    print(f"[CONFIG] Share publicly: {GRADIO_SHARE}")
    print("\n[INIT] Please wait while initializing...")
    print("\nNEW FEATURES:")
    print("1. [OK] Streaming responses")
    print("2. [OK] Multi-turn context")
    print("3. [OK] Response feedback")
    print("4. [OK] Chat history persistence")
    print("\nMake sure:")
    print("1. [OK] Vector database is built")
    print("2. [OK] Ollama is running (ollama serve)")
    print("3. [OK] Model is available (ollama pull gpt-oss:20b)")
    print("\n" + "="*60 + "\n")
    
    demo.launch(
        server_port=GRADIO_PORT,
        share=GRADIO_SHARE,
        show_error=True
    )

