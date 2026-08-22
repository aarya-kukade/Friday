# Kokoro TTS Integration Setup Guide

## Overview
Your FRIDAY application now integrates **Kokoro**, an advanced open-source text-to-speech engine with support for English and Hindi languages.

## Architecture

### Backend (Python/FastAPI)
- **Service**: `apps/api/core/kokoro_service.py` - Handles TTS synthesis
- **Routes**: `apps/api/api/routes/tts.py` - Exposes TTS endpoints
- **Endpoint**: `POST /api/tts/synthesize` - Generates audio from text

### Frontend (React/TypeScript)
- **Service**: `desktop/src/services/voiceService.ts` - Updated for Kokoro integration
- **Settings**: `desktop/src/components/voice/VoiceSettings.tsx` - Voice configuration panel
- **Store**: `desktop/src/store/voiceStore.ts` - Voice state management
- **Types**: `desktop/src/types/voice.ts` - Enhanced with language/voice configs

## Installation & Setup

### 1. Backend Setup

#### Install Kokoro Package
```bash
cd apps/api
pip install kokoro-tts
# or for specific version
pip install kokoro-tts==0.2.1
```

#### Install Dependencies
```bash
pip install fastapi uvicorn pydantic python-multipart
```

#### Verify Installation
```bash
python -c "import kokoro; print('Kokoro installed successfully')"
```

### 2. Frontend Setup

#### Install React Dependencies
```bash
cd desktop
npm install
# or
yarn install
```

The frontend already includes all necessary dependencies for voice synthesis.

### 3. Environment Configuration

#### Backend (.env in `apps/api/`)
```env
# Optional: API configuration
API_HOST=0.0.0.0
API_PORT=8000
```

#### Frontend (.env.local in `desktop/`)
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Usage

### Starting the Application

#### Terminal 1: Backend API
```bash
cd apps/api
python main.py
# Server runs on http://0.0.0.0:8000
```

#### Terminal 2: Frontend Application
```bash
cd desktop
npm run dev
# Application runs on http://localhost:3000
```

### Available Endpoints

#### 1. Synthesize Speech
```
POST /api/tts/synthesize
Content-Type: application/json

{
  "text": "Hello, how can I help you?",
  "voice": "af_bella",
  "language": "en",
  "speed": 1.0
}
```

**Response**: WAV audio file (audio/wav)

#### 2. Get Available Voices
```
GET /api/tts/voices?language=en
```

**Response**:
```json
{
  "language": "en",
  "voice": "af_bella",
  "available_voices": {
    "abreeze": {"name": "Abreeze", "gender": "female", "lang": "en"},
    "bella": {"name": "Bella", "gender": "female", "lang": "en"},
    ...
  }
}
```

#### 3. Get All Voices
```
GET /api/tts/voices/all
```

## Voice Options

### English Voices
| Voice Code | Name | Gender |
|-----------|------|--------|
| af_bella | Bella | Female |
| af_abreeze | Abreeze | Female |
| af_sarah | Sarah | Female |
| af_nicole | Nicole | Female |
| am_alpha | Alpha | Male |
| am_charlie | Charlie | Male |
| am_josh | Josh | Male |

### Hindi Voices
| Voice Code | Name | Gender |
|-----------|------|--------|
| hi_maya | Maya | Female |
| hi_arjun | Arjun | Male |

## Frontend Features

### Voice Settings Panel
- **Language Selection**: Switch between English 🇬🇧 and Hindi 🇮🇳
- **Voice Selection**: Choose from available voices for selected language
- **Speed Control**: Adjust speech speed (0.5x - 2.0x)
- **Voice Testing**: Test selected voice with sample text
- **Persistent Settings**: Settings are stored in Zustand store

### Integration Points
1. **Voice Command Response**: Automatically speaks responses in configured language/voice
2. **Settings Icon**: Click settings to open voice configuration panel
3. **Language Support**: Commands are processed in English, responses in selected language

## Configuration & Customization

### Change Default Voice
Edit `desktop/src/store/voiceStore.ts`:
```typescript
currentVoice: 'af_bella',  // Change to your preferred voice
language: 'en',            // Default language
ttsSpeed: 1.0,            // Default speed
```

### Add New Voices
1. Update `apps/api/core/kokoro_service.py` - Add to `VoiceCharacter` enum
2. Update `desktop/src/components/voice/VoiceSettings.tsx` - Add to default voices

### Customize API URL
Edit `desktop/src/services/fileService.ts`:
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
```

## Troubleshooting

### Issue: "Kokoro TTS is not available"
**Solution**: Install Kokoro package
```bash
pip install kokoro-tts
```

### Issue: CORS Errors
**Solution**: Verify CORS settings in `apps/api/main.py`:
```python
allow_origins=["http://localhost:3000", "http://localhost:3001"],
```

### Issue: Audio not playing
**Solution**: 
1. Check browser console for errors
2. Verify API endpoint is reachable
3. Test with curl: `curl http://127.0.0.1:8000/api/tts/voices`

### Issue: Voice recognition not working
**Solution**:
1. Ensure microphone permission is granted
2. Use Chrome or Edge browser
3. Use localhost (not 127.0.0.1 for some browsers)

## Code Examples

### Using VoiceService Directly

```typescript
import { voiceService } from '@/services/voiceService';

// Set language and voice
voiceService.setLanguage('hi');
voiceService.setVoice('hi_maya');

// Speak text
await voiceService.speak('नमस्ते, मैं FRIDAY हूं', () => {
  console.log('Speech finished');
});

// Get available voices
const voices = await voiceService.getAvailableVoices('en');
console.log(voices);
```

### Using Zustand Store

```typescript
import { useVoiceStore } from '@/store/voiceStore';

const store = useVoiceStore();

// Update configuration
store.setLanguage('en');
store.setCurrentVoice('af_bella');
store.setTtsSpeed(1.2);

// Access configuration
console.log(store.language);
console.log(store.currentVoice);
```

### Backend API Call

```python
from apps.api.core.kokoro_service import kokoro_service

# Synthesize speech
audio_bytes, mime_type = kokoro_service.synthesize(
    text="नमस्ते",
    voice="hi_maya",
    language="hi",
    speed=1.0
)

# Save or stream audio
with open("output.wav", "wb") as f:
    f.write(audio_bytes)
```

## Performance Notes

- **Synthesis Speed**: Typical synthesis takes 0.5-2 seconds depending on text length
- **Audio Quality**: 24kHz mono WAV format
- **Memory Usage**: ~200MB for Kokoro models (loaded on first use)
- **Caching**: Consider implementing audio caching for frequently used phrases

## Security Considerations

- API endpoint has CORS protection
- Text input is validated and sanitized
- No sensitive data is logged
- Audio is generated server-side

## Future Enhancements

- [ ] Audio caching for repeated phrases
- [ ] Batch synthesis API
- [ ] Voice emotion/style parameters
- [ ] Regional language support (Tamil, Telugu, etc.)
- [ ] Real-time streaming synthesis
- [ ] Voice customization (pitch, intonation)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API logs: `tail -f logs/api.log`
3. Test endpoints with curl or Postman
4. Check browser console for frontend errors

---

**Last Updated**: 2024
**Kokoro Version**: Latest
**Language Support**: English (en), Hindi (hi)
