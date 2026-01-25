# Voice Note Transcription

## Setup

Voice note transcription is configured using OpenAI Whisper API.

### Prerequisites
- ✅ ffmpeg installed
- ✅ OpenAI SDK installed (`pip install openai`)
- ✅ API key stored in `/root/clawd/.env`

### Configuration

API key location: `/root/clawd/.env`

```env
OPENAI_API_KEY=sk-proj-...
```

### Scripts

- **`transcribe-voice-note.py`** - Manual transcription tool
- **`handle-voice-note.py`** - Auto-handler for Clawdbot integration

### Usage

**Manual transcription:**
```bash
cd /root/clawd
python3 transcribe-voice-note.py /path/to/voice-note.ogg
```

**Auto-transcription (via Clawdbot):**
Just send a voice note on WhatsApp — Clawdbot will automatically transcribe it and treat the transcript as your message.

### Cost

OpenAI Whisper API pricing: **$0.006 per minute**

Examples:
- 1 minute voice note = $0.006
- 10 minutes = $0.06
- 100 minutes = $0.60
- 1,000 minutes (16.7 hours) = $6

Very affordable for regular use.

### Supported Formats

- `.ogg` (WhatsApp default)
- `.mp3`
- `.mp4`
- `.wav`
- `.m4a`

Whisper API handles format conversion automatically.

### Language Support

Currently configured for English, but Whisper supports 50+ languages. Can auto-detect or specify language code.

### Privacy

- Audio files sent to OpenAI for transcription
- Not stored/used for training (per OpenAI API policy)
- Transcripts processed in memory
- Original audio files stored locally in Clawdbot media cache

---

**Status:** ✅ Live and working
