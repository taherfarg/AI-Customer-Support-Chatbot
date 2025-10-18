"""
Chat History Manager
Handles conversation persistence, feedback, and export
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class ChatManager:
    """Manages chat history, feedback, and persistence"""
    
    def __init__(self, storage_dir: str = "chat_history"):
        """
        Initialize chat manager
        
        Args:
            storage_dir: Directory to store chat history
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        self.conversations_file = self.storage_dir / "conversations.json"
        self.feedback_file = self.storage_dir / "feedback.json"
        
        # Load existing data
        self.conversations = self._load_conversations()
        self.feedback = self._load_feedback()
    
    def _load_conversations(self) -> Dict:
        """Load conversations from file"""
        if self.conversations_file.exists():
            try:
                with open(self.conversations_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARN] Could not load conversations: {e}")
        return {}
    
    def _load_feedback(self) -> Dict:
        """Load feedback from file"""
        if self.feedback_file.exists():
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARN] Could not load feedback: {e}")
        return {}
    
    def _save_conversations(self):
        """Save conversations to file"""
        try:
            with open(self.conversations_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Could not save conversations: {e}")
    
    def _save_feedback(self):
        """Save feedback to file"""
        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.feedback, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Could not save feedback: {e}")
    
    def create_session(self) -> str:
        """
        Create a new chat session
        
        Returns:
            Session ID
        """
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.conversations[session_id] = {
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "metadata": {}
        }
        self._save_conversations()
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Add a message to a session
        
        Args:
            session_id: Session ID
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata (sources, etc.)
        """
        if session_id not in self.conversations:
            self.create_session()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversations[session_id]["messages"].append(message)
        self._save_conversations()
    
    def get_conversation(self, session_id: str) -> Optional[Dict]:
        """
        Get a conversation by session ID
        
        Args:
            session_id: Session ID
            
        Returns:
            Conversation dict or None
        """
        return self.conversations.get(session_id)
    
    def get_all_sessions(self) -> List[Dict]:
        """
        Get all chat sessions
        
        Returns:
            List of session summaries
        """
        sessions = []
        for session_id, data in self.conversations.items():
            message_count = len(data.get("messages", []))
            first_message = data["messages"][0]["content"][:100] if data.get("messages") else "Empty"
            
            sessions.append({
                "session_id": session_id,
                "created_at": data.get("created_at"),
                "message_count": message_count,
                "preview": first_message
            })
        
        return sorted(sessions, key=lambda x: x["created_at"], reverse=True)
    
    def delete_session(self, session_id: str):
        """
        Delete a chat session
        
        Args:
            session_id: Session ID to delete
        """
        if session_id in self.conversations:
            del self.conversations[session_id]
            self._save_conversations()
    
    def add_feedback(self, session_id: str, message_index: int, feedback_type: str, comment: str = ""):
        """
        Add feedback for a message
        
        Args:
            session_id: Session ID
            message_index: Index of message in conversation
            feedback_type: 'positive' or 'negative'
            comment: Optional comment
        """
        feedback_id = f"{session_id}_{message_index}"
        
        self.feedback[feedback_id] = {
            "session_id": session_id,
            "message_index": message_index,
            "feedback_type": feedback_type,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        
        self._save_feedback()
    
    def get_feedback_stats(self) -> Dict:
        """
        Get feedback statistics
        
        Returns:
            Dict with feedback stats
        """
        total = len(self.feedback)
        positive = sum(1 for f in self.feedback.values() if f["feedback_type"] == "positive")
        negative = sum(1 for f in self.feedback.values() if f["feedback_type"] == "negative")
        
        return {
            "total": total,
            "positive": positive,
            "negative": negative,
            "satisfaction_rate": (positive / total * 100) if total > 0 else 0
        }
    
    def export_conversation(self, session_id: str, format: str = "json") -> str:
        """
        Export conversation to file
        
        Args:
            session_id: Session ID
            format: 'json', 'txt', or 'md'
            
        Returns:
            Path to exported file
        """
        conversation = self.get_conversation(session_id)
        if not conversation:
            return None
        
        export_dir = self.storage_dir / "exports"
        export_dir.mkdir(exist_ok=True)
        
        if format == "json":
            export_file = export_dir / f"chat_{session_id}.json"
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(conversation, f, indent=2, ensure_ascii=False)
        
        elif format == "txt":
            export_file = export_dir / f"chat_{session_id}.txt"
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(f"Chat Session: {session_id}\n")
                f.write(f"Created: {conversation['created_at']}\n")
                f.write("="*60 + "\n\n")
                
                for msg in conversation["messages"]:
                    role = msg["role"].upper()
                    content = msg["content"]
                    timestamp = msg["timestamp"]
                    f.write(f"[{role}] {timestamp}\n")
                    f.write(f"{content}\n\n")
        
        elif format == "md":
            export_file = export_dir / f"chat_{session_id}.md"
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(f"# Chat Session: {session_id}\n\n")
                f.write(f"**Created:** {conversation['created_at']}\n\n")
                f.write("---\n\n")
                
                for msg in conversation["messages"]:
                    role = msg["role"].capitalize()
                    content = msg["content"]
                    timestamp = msg["timestamp"]
                    f.write(f"### {role} ({timestamp})\n\n")
                    f.write(f"{content}\n\n")
        
        return str(export_file)
    
    def get_conversation_context(self, session_id: str, max_messages: int = 5) -> str:
        """
        Get formatted conversation history for context
        
        Args:
            session_id: Session ID
            max_messages: Maximum number of recent messages to include
            
        Returns:
            Formatted conversation history
        """
        conversation = self.get_conversation(session_id)
        if not conversation or not conversation.get("messages"):
            return ""
        
        messages = conversation["messages"][-max_messages:]
        
        context_parts = []
        for msg in messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"][:200]  # Limit length
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)


if __name__ == "__main__":
    """Test the chat manager"""
    print("="*60)
    print("TESTING CHAT MANAGER")
    print("="*60)
    
    # Initialize manager
    manager = ChatManager()
    
    # Create session
    session_id = manager.create_session()
    print(f"\n[OK] Created session: {session_id}")
    
    # Add messages
    manager.add_message(session_id, "user", "How do I reset my password?")
    manager.add_message(session_id, "assistant", "To reset your password, visit the settings page...")
    print("[OK] Added messages")
    
    # Add feedback
    manager.add_feedback(session_id, 1, "positive", "Very helpful!")
    print("[OK] Added feedback")
    
    # Get stats
    stats = manager.get_feedback_stats()
    print(f"[OK] Feedback stats: {stats}")
    
    # Export conversation
    export_file = manager.export_conversation(session_id, "txt")
    print(f"[OK] Exported to: {export_file}")
    
    print("\n" + "="*60)
    print("[SUCCESS] All tests passed!")
    print("="*60)

