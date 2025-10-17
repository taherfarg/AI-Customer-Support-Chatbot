"""
Voice Utilities for RAG Chatbot
Handles Speech-to-Text (STT) and Text-to-Speech (TTS)
Compatible with Python 3.13+
"""

import os
import tempfile
from pathlib import Path
from gtts import gTTS
import io

# Handle Python 3.13 compatibility for speech_recognition
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    print(f"Warning: speech_recognition not fully compatible: {e}")
    print("Voice input will be limited. Text-to-speech still available.")
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None


class VoiceHandler:
    """Handle voice input and output for the chatbot"""
    
    def __init__(self):
        """Initialize voice handler"""
        self.recognizer = sr.Recognizer() if SPEECH_RECOGNITION_AVAILABLE else None
        self.temp_dir = tempfile.gettempdir()
        self.stt_available = SPEECH_RECOGNITION_AVAILABLE
    
    def speech_to_text(self, audio_path):
        """
        Convert speech audio file to text
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text or error message
        """
        if not self.stt_available:
            return None, "Speech recognition not available (Python 3.13 compatibility issue). Please use text input."
        
        try:
            # Load audio file
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Record audio
                audio_data = self.recognizer.record(source)
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio_data)
            return text, None
            
        except sr.UnknownValueError:
            return None, "Could not understand audio. Please speak clearly and try again."
        except sr.RequestError as e:
            return None, f"Speech recognition service error: {e}"
        except Exception as e:
            return None, f"Error processing audio: {e}"
    
    def text_to_speech(self, text, lang='en'):
        """
        Convert text to speech audio file
        
        Args:
            text: Text to convert to speech
            lang: Language code (default: 'en')
            
        Returns:
            Path to generated audio file or None if error
        """
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=lang, slow=False)
            
            # Generate unique filename
            audio_file = os.path.join(self.temp_dir, f"chatbot_response_{os.getpid()}.mp3")
            
            # Save to file
            tts.save(audio_file)
            
            return audio_file, None
            
        except Exception as e:
            return None, f"Error generating speech: {e}"
    
    def microphone_to_text(self):
        """
        Capture audio from microphone and convert to text
        
        Returns:
            Transcribed text or error message
        """
        if not self.stt_available:
            return None, "Speech recognition not available (Python 3.13 compatibility issue). Please use text input or record audio files."
        
        try:
            with sr.Microphone() as source:
                print("🎤 Listening... (speak now)")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen to audio
                audio_data = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("🔄 Processing...")
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio_data)
            return text, None
            
        except sr.WaitTimeoutError:
            return None, "No speech detected. Please try again."
        except sr.UnknownValueError:
            return None, "Could not understand audio. Please speak clearly."
        except sr.RequestError as e:
            return None, f"Speech recognition error: {e}"
        except Exception as e:
            return None, f"Error: {e}"


def test_voice_handler():
    """Test the voice handler"""
    print("="*60)
    print("VOICE HANDLER TEST")
    print("="*60)
    
    handler = VoiceHandler()
    
    # Check STT availability
    if handler.stt_available:
        print("[OK] Speech-to-Text: Available")
    else:
        print("[WARN] Speech-to-Text: Not available (Python 3.13 compatibility)")
        print("       Text-to-Speech will still work!")
    
    # Test TTS
    print("\nTesting Text-to-Speech...")
    test_text = "Hello! This is a test of the text to speech system. How are you today?"
    audio_file, error = handler.text_to_speech(test_text)
    
    if error:
        print(f"[ERROR] TTS Error: {error}")
    else:
        print(f"[SUCCESS] TTS Success! Audio saved to: {audio_file}")
        print(f"          You can play this file to hear the test.")
    
    print("\n" + "="*60)
    print("Voice handler initialized!")
    print("="*60)


if __name__ == "__main__":
    test_voice_handler()

