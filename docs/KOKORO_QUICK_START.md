# Kokoro TTS - Quick Reference Guide

## Overview
Kokoro is an open-source text-to-speech engine integrated into FRIDAY with support for:
- **English (en)**: 7 voices (4 female, 3 male)
- **Hindi (hi)**: 2 voices (1 female, 1 male)

## Installation (One-time Setup)

### Step 1: Install Backend Dependencies
```bash
cd apps/api
pip install -r requirements.txt
```

Or manually:
```bash
pip install kokoro-tts fastapi uvicorn pydantic numpy
```

### Step 2: Start Backend API
```bash
cd apps/api
python main.py
```
✅ API running on http://localhost:8000

### Step 3: Start Frontend
```bash
cd desktop
npm install  # if not done yet
npm run dev
```
✅ App running on http://localhost:3000

## Using Kokoro TTS

### From the UI
1. **Open Voice Settings**: Click the settings icon (⚙️) in the interface
2. **Select Language**: Choose English (🇬🇧) or Hindi (🇮🇳)
3. **Select Voice**: Pick your preferred voice from the dropdown
4. **Adjust Speed**: Use slider to control speech speed (0.5x - 2.0x)
5. **Test Voice**: Click "🔊 Test Voice" to hear the selected voice
6. **Close Settings**: Click "Close" to save preferences

### Programmatically (TypeScript/React)

#### Example 1: Using the VoiceService
```typescript
import { voiceService } from '@/services/voiceService';

// Set language and voice
voiceService.setLanguage('hi');
voiceService.setVoice('hi_maya');

// Speak in Hindi
await voiceService.speak('नमस्ते, मैं FRIDAY हूं', () => {
  console.log('Speech complete');
});
```

#### Example 2: Using the Zustand Store
```typescript
import { useVoiceStore } from '@/store/voiceStore';

export const MyComponent = () => {
  const store = useVoiceStore();

  const handleChangeLanguage = () => {
    store.setLanguage('hi');
    store.setCurrentVoice('hi_maya');
  };

  return (
    <button onClick={handleChangeLanguage}>
      Switch to Hindi - Maya Voice
    </button>
  );
};
```

#### Example 3: Custom Speech
```typescript
import { voiceService } from '@/services/voiceService';

// Speak in Hindi with custom voice
const speakInHindi = async (text: string) => {
  await voiceService.speak(
    text,
    () => console.log('Done'),
    'hi',           // language
    'hi_maya'       // voice
  );
};

// Usage
speakInHindi('आपका स्वागत है');
```

### From Python Backend

```python
from apps.api.core.kokoro_service import kokoro_service

# Synthesize English
audio_en, mime = kokoro_service.synthesize(
    text="Hello, welcome to FRIDAY",
    voice="af_bella",
    language="en"
)

# Synthesize Hindi
audio_hi, mime = kokoro_service.synthesize(
    text="नमस्ते, FRIDAY में आपका स्वागत है",
    voice="hi_maya",
    language="hi"
)

# Save or send over network
with open("english.wav", "wb") as f:
    f.write(audio_en)
```

## API Endpoints Reference

### 1. Synthesize Speech
```bash
POST /api/tts/synthesize
Content-Type: application/json

{
  "text": "Hello world",
  "voice": "af_bella",
  "language": "en",
  "speed": 1.0
}
```
Returns: WAV audio file

### 2. List Voices by Language
```bash
GET /api/tts/voices?language=en
```
Returns: All available voices for English

### 3. List All Voices
```bash
GET /api/tts/voices/all
```
Returns: All voices for all languages

## Voice Codes Reference

### English Voices
| Code | Name | Gender | Sample |
|------|------|--------|--------|
| af_bella | Bella | Female | Friendly, clear |
| af_abreeze | Abreeze | Female | Cheerful |
| af_sarah | Sarah | Female | Professional |
| af_nicole | Nicole | Female | Warm |
| am_alpha | Alpha | Male | Deep, authoritative |
| am_charlie | Charlie | Male | Natural |
| am_josh | Josh | Male | Casual |

### Hindi Voices
| Code | Name | Gender | Sample |
|------|------|--------|--------|
| hi_maya | Maya | Female | Natural Hindi |
| hi_arjun | Arjun | Male | Native Hindi |

## Common Tasks

### Task 1: Set Default Voice to Hindi Maya
Edit `desktop/src/store/voiceStore.ts`:
```typescript
language: 'hi',
currentVoice: 'hi_maya',
```

### Task 2: Test English Voice from Terminal
```bash
curl -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","voice":"af_bella","language":"en"}' \
  --output test.wav
```

### Task 3: Test Hindi Voice from Terminal
```bash
curl -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text":"नमस्ते","voice":"hi_maya","language":"hi"}' \
  --output test.wav
```

### Task 4: Get All Available Voices
```bash
curl http://localhost:8000/api/tts/voices/all | python -m json.tool
```

### Task 5: Voice Command in Hindi
1. In the UI, select Hindi language
2. Say a command (it will be recognized in English)
3. Response will be spoken in Hindi with selected voice

## Troubleshooting

### Problem: "Kokoro TTS is not available"
```bash
# Solution: Install Kokoro
pip install kokoro-tts
```

### Problem: No audio playing
1. Check browser console for errors (F12)
2. Verify API is running: `curl http://localhost:8000/health`
3. Check CORS settings in `apps/api/main.py`

### Problem: Voice command not working
1. Ensure microphone permission is granted
2. Use Chrome or Edge browser
3. Use localhost (not 127.0.0.1)
4. Check browser console for errors

### Problem: Slow first synthesis
- Normal! First call loads Kokoro models (~200MB)
- Subsequent calls are much faster
- Consider pre-loading or caching

### Problem: Wrong language synthesis
1. Verify language code: 'en' or 'hi'
2. Check if text is in correct language
3. Restart backend: `Ctrl+C` then `python main.py`

## Configuration

### Default Settings
```typescript
language: 'en'              // Default to English
currentVoice: 'af_bella'    // Default to Bella
ttsSpeed: 1.0               // Normal speed
```

### Change Defaults
Edit `desktop/src/store/voiceStore.ts` and restart frontend:
```typescript
language: 'hi',
currentVoice: 'hi_maya',
ttsSpeed: 1.2,
```

### API Configuration
Edit `apps/api/main.py` for CORS:
```python
allow_origins=[
  "http://localhost:3000",
  "http://localhost:3001",
  "http://yourapp.com"  # Add custom domain
],
```

## Performance Tips

1. **First Call**: Kokoro loads models (~200MB) - takes ~2-3 seconds
2. **Subsequent Calls**: Fast synthesis - ~0.5-1 second
3. **Memory**: ~200MB for models in memory
4. **Caching**: Use same voice repeatedly for better performance

## Advanced: Custom Voice Settings

### Add to Voice Settings Component
```typescript
// In VoiceSettings.tsx
const handleCustomSpeed = (speed: number) => {
  store.setTtsSpeed(speed);
  voiceService.speak("Test", undefined, store.language, store.currentVoice);
};
```

## Language Support Matrix

| Feature | English | Hindi | Status |
|---------|---------|-------|--------|
| Text Synthesis | ✅ | ✅ | Ready |
| Multiple Voices | ✅ (7) | ✅ (2) | Ready |
| Speed Control | ✅ | ✅ | Ready |
| Voice Selection | ✅ | ✅ | Ready |
| Voice Commands | ✅ | ✅ | Ready |

## Next Steps

1. ✅ Install and run backend + frontend
2. ✅ Open voice settings and select language
3. ✅ Test different voices
4. ✅ Try voice commands in English
5. ✅ Listen to responses in your selected language

## Need Help?

- **Setup Issues**: See `KOKORO_SETUP.md`
- **API Docs**: See `apps/api/README.md`
- **Code**: Check comments in `core/kokoro_service.py`
- **Backend Logs**: Run `python main.py` in terminal
- **Frontend Logs**: Check browser console (F12)

---

**Happy Speaking! 🎤🇮🇳🇬🇧**
