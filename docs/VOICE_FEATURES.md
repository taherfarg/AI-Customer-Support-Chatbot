# 🎤 Voice Features Guide

## Overview

Your AI Customer Support Chatbot now supports **full voice interaction**!

### Features
- 🎤 **Speech-to-Text (STT)** - Speak your questions
- 🔊 **Text-to-Speech (TTS)** - Hear responses
- 🔄 **Dual Mode** - Use text OR voice seamlessly
- 🌐 **Google Speech Recognition** - Accurate transcription
- 🗣️ **Natural Voice** - High-quality gTTS voice output

---

## 🎯 How to Use Voice Features

### Method 1: Voice Input Only
1. Click the **microphone icon** in the "Speak Your Question" section
2. **Speak your question** clearly (e.g., "How do I reset my password?")
3. Click **"🎤 Send Voice"** button
4. Get **text response + voice playback**

### Method 2: Text Input with Voice Response
1. Type your question in the text box
2. Check the **"Voice Responses"** checkbox
3. Click **"Send 📤"**
4. Get text response + automatic voice playback

### Method 3: Text Only (Default)
1. Type your question
2. Leave "Voice Responses" unchecked
3. Get text-only response

---

## 🎙️ Voice Input Tips

### For Best Results:
- ✅ Speak clearly and at normal pace
- ✅ Use a good microphone (built-in is fine)
- ✅ Minimize background noise
- ✅ Keep questions concise (under 10 seconds)
- ✅ Ensure stable internet (uses Google Speech API)

### What to Say:
Instead of: "Um... I want to, like, reset my password?"
Say: "How do I reset my password?"

Instead of: "My payment... it didn't work... failed..."
Say: "My payment failed"

---

## 🔊 Voice Output Features

### Automatic Playback
- Voice responses are generated automatically
- Audio player appears below voice input
- Click play to hear the response
- Adjust volume with audio controls

### Smart Response
- Only reads the answer (not source citations)
- Natural-sounding voice
- Clear pronunciation
- Adjustable playback speed in audio player

---

## ⚙️ Technical Details

### Speech-to-Text (STT)
- **Engine:** Google Speech Recognition API
- **Language:** English (en-US)
- **Format:** WAV/Audio files
- **Accuracy:** High (95%+ for clear speech)
- **Requirements:** Internet connection

### Text-to-Speech (TTS)
- **Engine:** Google Text-to-Speech (gTTS)
- **Language:** English
- **Format:** MP3
- **Quality:** High-quality natural voice
- **Speed:** Normal (adjustable)

### Audio Processing
- **Input:** Microphone or audio file
- **Processing:** Real-time transcription
- **Output:** Downloadable MP3
- **Storage:** Temporary files (auto-cleanup)

---

## 🎮 UI Controls

### Voice Input Section
```
┌─────────────────────────────────────┐
│ 🎤 Voice Input                      │
├─────────────────────────────────────┤
│ [Microphone] Record your question   │
│ [🎤 Send Voice] Process & respond   │
└─────────────────────────────────────┘
```

### Voice Output Section
```
┌─────────────────────────────────────┐
│ 🔊 Voice Response                   │
├─────────────────────────────────────┤
│ [Audio Player] ▶️ Play/Pause       │
│ Volume: ━━━━●━━ Download 📥        │
└─────────────────────────────────────┘
```

### Control Options
- ☑️ **Show Sources** - Display similar conversations
- ☑️ **Voice Responses** - Enable TTS for text input
- 🗑️ **Clear Chat** - Reset conversation

---

## 🔧 Troubleshooting

### Voice Input Not Working

**Issue:** "Could not understand audio"
**Solutions:**
- Speak more clearly
- Reduce background noise
- Check microphone permissions
- Ensure internet connection

**Issue:** "Speech recognition service error"
**Solutions:**
- Check internet connection
- Try again in a few seconds
- Verify Google services are accessible

**Issue:** "No speech detected"
**Solutions:**
- Speak louder
- Check microphone is working
- Ensure mic is not muted
- Try shorter phrases

### Voice Output Not Working

**Issue:** No audio generated
**Solutions:**
- Check "Voice Responses" is enabled
- Verify internet connection
- Check browser audio permissions
- Try refreshing the page

**Issue:** Audio won't play
**Solutions:**
- Click the play button
- Check browser audio settings
- Verify volume is not muted
- Try downloading and playing locally

---

## 📊 Supported Scenarios

### ✅ Works Great For:
- Quick questions
- Password resets
- Account issues
- Payment problems
- General support queries
- Short conversations

### ⚠️ May Need Text For:
- Very long explanations
- Technical jargon
- Spelling-specific queries
- Multi-step instructions
- Reading detailed documentation

---

## 🎯 Example Voice Interactions

### Example 1: Password Reset
**You (speaking):** "How do I reset my password?"
**Chatbot (text + voice):** "To reset your password, go to the login page and click 'Forgot Password'..."

### Example 2: Payment Issue
**You (speaking):** "My payment failed"
**Chatbot (text + voice):** "If your payment failed, please try the following steps..."

### Example 3: Account Help
**You (speaking):** "I can't log into my account"
**Chatbot (text + voice):** "Let me help you with your login issue..."

---

## 🌟 Pro Tips

1. **Use Voice for Quick Questions**
   - Faster than typing
   - Natural conversation flow
   - Great for mobile devices

2. **Enable Voice Responses for Accessibility**
   - Helps visually impaired users
   - Multitask while listening
   - Better for on-the-go support

3. **Combine Both Modes**
   - Speak question, read detailed response
   - Type complex queries, hear summary
   - Switch modes as needed

4. **Download Voice Responses**
   - Save important instructions
   - Listen offline later
   - Share with others

---

## 🔐 Privacy & Security

### Voice Data
- 🔒 Processed via Google APIs
- 🔒 Not stored permanently
- 🔒 Temporary audio files auto-deleted
- 🔒 No voice profiling or training

### Audio Files
- 📁 Stored in system temp folder
- ⏱️ Auto-cleanup after session
- 🗑️ Clear with "Clear Chat" button
- 💾 Download option available

---

## 📱 Device Compatibility

### Desktop
- ✅ Windows (Tested)
- ✅ macOS
- ✅ Linux

### Browsers
- ✅ Chrome (Best)
- ✅ Edge
- ✅ Firefox
- ✅ Safari
- ⚠️ Requires microphone permissions

### Mobile
- ✅ iOS Safari
- ✅ Android Chrome
- ℹ️ May require browser permissions

---

## 🚀 Advanced Usage

### API Access
Use voice features programmatically:

```python
from voice_utils import VoiceHandler

handler = VoiceHandler()

# Speech to text
text, error = handler.speech_to_text("audio.wav")
print(f"You said: {text}")

# Text to speech
audio_file, error = handler.text_to_speech("Hello, how can I help?")
print(f"Audio saved: {audio_file}")
```

### Custom Settings
Modify `voice_utils.py` for:
- Different languages
- Voice speed
- Audio quality
- Alternative TTS engines

---

## 📞 Support

### Getting Help
If voice features aren't working:
1. Check the troubleshooting section above
2. Verify all dependencies are installed:
   ```bash
   pip install speechrecognition gTTS pyaudio
   ```
3. Test voice utilities:
   ```bash
   python voice_utils.py
   ```
4. Check browser console for errors

### Requirements
- ✅ Python packages: `speechrecognition`, `gTTS`, `pyaudio`
- ✅ Internet connection (for Google APIs)
- ✅ Microphone access
- ✅ Audio output device
- ✅ Modern web browser

---

**Enjoy hands-free customer support! 🎤🤖**

