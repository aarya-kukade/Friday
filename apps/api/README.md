# FRIDAY Backend - Kokoro TTS Integration

## Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the API Server**
```bash
python main.py
```

The API will start on `http://0.0.0.0:8000`

### API Endpoints

#### Text-to-Speech Synthesis
```bash
curl -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "voice": "af_bella",
    "language": "en",
    "speed": 1.0
  }' \
  --output audio.wav
```

#### Get Available Voices
```bash
curl http://localhost:8000/api/tts/voices?language=en
```

#### Get All Voices
```bash
curl http://localhost:8000/api/tts/voices/all
```

## Project Structure

```
apps/api/
├── main.py                           # FastAPI application entry point
├── requirements.txt                  # Python dependencies
├── api/
│   └── routes/
│       ├── files.py                 # File operation endpoints
│       ├── voice_commands.py        # Voice command endpoints
│       └── tts.py                   # Text-to-speech endpoints (NEW)
└── core/
    ├── command_parser.py            # Voice command parsing
    ├── database.py                  # Database utilities
    ├── file_operations.py           # File operation handlers
    ├── init_db.py                   # Database initialization
    └── kokoro_service.py            # Kokoro TTS service (NEW)
```

## Configuration

### Environment Variables

Add to `.env` file (optional):
```env
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### CORS Settings

Edit `main.py` to modify allowed origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Available Voices

### English (en)
- **af_bella** (Female) - Default
- **af_abreeze** (Female)
- **af_sarah** (Female)
- **af_nicole** (Female)
- **am_alpha** (Male)
- **am_charlie** (Male)
- **am_josh** (Male)

### Hindi (hi)
- **hi_maya** (Female)
- **hi_arjun** (Male)

## API Documentation

### Synthesize Speech

**Endpoint**: `POST /api/tts/synthesize`

**Request Body**:
```json
{
  "text": "Text to synthesize",
  "voice": "af_bella",
  "language": "en",
  "speed": 1.0
}
```

**Parameters**:
- `text` (string, required): The text to convert to speech
- `voice` (string, optional): Voice code (default: "af_bella")
- `language` (string, optional): Language code "en" or "hi" (default: "en")
- `speed` (number, optional): Speech speed multiplier 0.5-2.0 (default: 1.0)

**Response**: WAV audio file (audio/wav)

**Errors**:
- 400: Invalid parameters
- 503: Kokoro service not available
- 500: Synthesis error

### Get Available Voices

**Endpoint**: `GET /api/tts/voices?language={language}`

**Query Parameters**:
- `language` (string, optional): "en" or "hi" (default: "en")

**Response**:
```json
{
  "language": "en",
  "voice": "af_bella",
  "available_voices": {
    "bella": {
      "name": "Bella",
      "gender": "female",
      "lang": "en"
    }
  }
}
```

### Get All Voices

**Endpoint**: `GET /api/tts/voices/all`

**Response**:
```json
{
  "en": {
    "bella": {"name": "Bella", "gender": "female", "lang": "en"}
  },
  "hi": {
    "maya": {"name": "Maya", "gender": "female", "lang": "hi"}
  }
}
```

## Voice Command Integration

The TTS service integrates with voice commands. When a voice command is executed:

1. Command is transcribed using Web Speech API
2. Sent to `/api/voice/execute` endpoint for processing
3. Response is synthesized using Kokoro TTS
4. Audio is played using the configured voice and language

Example flow:
```
User says: "Create a file"
  ↓
Transcribed: "create a file"
  ↓
Backend processes command
  ↓
Response: "File created successfully"
  ↓
Kokoro TTS synthesizes response in user's selected voice/language
  ↓
Audio plays in browser
```

## Development

### Adding New Voices

1. Update `VoiceCharacter` enum in `core/kokoro_service.py`
2. Update voice list in `get_available_voices()` method
3. Restart API server

### Extending TTS Service

Add new methods to `KokoroService` class:

```python
def custom_synthesis(self, **kwargs):
    """Custom synthesis logic"""
    pass
```

### Testing the API

```bash
# Test synthesize endpoint
curl -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Test", "voice": "af_bella"}' \
  --output test.wav

# Test voices endpoint
curl http://localhost:8000/api/tts/voices

# Test all voices endpoint
curl http://localhost:8000/api/tts/voices/all

# Check API health
curl http://localhost:8000/health
```

## Troubleshooting

### Import Error: "No module named 'kokoro'"

**Solution**: Install Kokoro package
```bash
pip install kokoro-tts
```

### Connection refused error

**Solution**: Ensure API is running and port 8000 is available
```bash
python main.py
```

### Slow response times

**Solution**: 
- First synthesis is slower (model loading)
- Subsequent requests are faster
- Consider implementing caching for common phrases

### CORS errors from frontend

**Solution**: 
1. Verify frontend URL is in `allow_origins`
2. Check that frontend is running on correct port
3. Clear browser cache and restart

## Performance Optimization

- **Model Caching**: Models are loaded once and reused
- **Audio Streaming**: Large audio files are streamed to client
- **Async Operations**: All endpoints are async for better performance
- **Connection Pooling**: CORS middleware handles concurrent requests

## Security

- All text input is validated
- No sensitive data is logged
- CORS protection prevents unauthorized access
- Input size limits prevent DoS attacks

## Deployment

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t friday-api .
docker run -p 8000:8000 friday-api
```

### Production Considerations

- Use Gunicorn with multiple workers
- Enable HTTPS/SSL
- Implement rate limiting
- Add authentication for API endpoints
- Monitor memory usage (Kokoro models)
- Implement audio caching

## Next Steps

1. **Frontend Integration**: Start the Next.js frontend (`desktop/npm run dev`)
2. **Voice Configuration**: Access voice settings through the UI
3. **Test End-to-End**: Record a voice command and hear the response
4. **Customize**: Modify voices and language preferences in settings

## Support & Documentation

- See `KOKORO_SETUP.md` for detailed setup guide
- Check `docs/` folder for additional documentation
- Review code comments in `core/kokoro_service.py` for implementation details

---

**Backend Version**: 0.1.0  
**Kokoro TTS**: Latest  
**Language Support**: English, Hindi
