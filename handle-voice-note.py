#!/usr/bin/env python3
"""
Auto-handler for WhatsApp voice notes
Called by Clawdbot when a voice note arrives
"""

import os
import sys
from pathlib import Path
from openai import OpenAI

# Load API key from .env
env_file = Path(__file__).parent / '.env'
api_key = None
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                api_key = line.strip().split('=', 1)[1]
                break

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env")
    sys.exit(1)

client = OpenAI(api_key=api_key)

def transcribe_voice_note(audio_path):
    """Transcribe voice note and return text"""
    try:
        with open(audio_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        return f"[Transcription failed: {e}]"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: handle-voice-note.py <audio-file-path>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    if not Path(audio_path).exists():
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)
    
    # Transcribe
    transcript = transcribe_voice_note(audio_path)
    
    # Output transcript (Clawdbot will see this as the message content)
    print(f"🎤 Transcription:\n{transcript}")
