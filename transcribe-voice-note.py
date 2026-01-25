#!/usr/bin/env python3
"""
Voice note transcription using OpenAI Whisper API
"""

import os
import sys
from pathlib import Path
from openai import OpenAI

# Load API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    # Try loading from .env file
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    api_key = line.strip().split('=', 1)[1]
                    break

if not api_key:
    print("Error: OPENAI_API_KEY not found")
    sys.exit(1)

client = OpenAI(api_key=api_key)

def transcribe_audio(audio_path):
    """Transcribe audio file using OpenAI Whisper API"""
    audio_path = Path(audio_path)
    
    if not audio_path.exists():
        return f"Error: File not found: {audio_path}"
    
    try:
        with open(audio_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"  # Can be auto-detected by leaving this out
            )
        return transcript.text
    except Exception as e:
        return f"Error transcribing: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: transcribe-voice-note.py <audio-file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    result = transcribe_audio(audio_file)
    print(result)
