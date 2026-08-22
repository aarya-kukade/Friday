from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from apps.api.core.kokoro_service import kokoro_service
import io

router = APIRouter(prefix="/api/tts", tags=["text-to-speech"])


class TTSRequest(BaseModel):
    """Text-to-Speech synthesis request"""
    text: str
    voice: str = "af_bella"  # Default female voice (Bella) in English
    language: str = "en"  # Language: "en" (English) or "hi" (Hindi)
    speed: float = 1.0  # Speech speed multiplier


class VoiceInfo(BaseModel):
    """Voice information response"""
    language: str
    voice: str
    available_voices: dict


@router.post("/synthesize")
async def synthesize_speech(request: TTSRequest) -> StreamingResponse:
    """
    Synthesize speech from text using Kokoro TTS

    Example:
    {
        "text": "Hello, how can I help you?",
        "voice": "af_bella",
        "language": "en",
        "speed": 1.0
    }
    """
    try:
        if not kokoro_service.is_available:
            raise HTTPException(
                status_code=503,
                detail="Kokoro TTS service is not available. Please install it."
            )

        # Validate language
        if request.language not in ["en", "hi"]:
            raise HTTPException(
                status_code=400,
                detail="Language must be 'en' (English) or 'hi' (Hindi)"
            )

        # Validate speed
        if not (0.5 <= request.speed <= 2.0):
            raise HTTPException(
                status_code=400,
                detail="Speed must be between 0.5 and 2.0"
            )

        # Synthesize audio
        audio_bytes, mime_type, is_fallback = kokoro_service.synthesize(
            text=request.text,
            voice=request.voice,
            language=request.language,
            speed=request.speed,
        )

        headers = {"Content-Disposition": "attachment; filename=audio.wav"}
        if is_fallback:
            headers["X-Kokoro-Fallback"] = "true"

        return StreamingResponse(
            iter([audio_bytes]),
            media_type=mime_type,
            headers=headers
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synthesis error: {str(e)}")


@router.get("/voices")
async def get_voices(language: str = "en") -> VoiceInfo:
    """
    Get available voices for a language

    Query parameters:
    - language: "en" (English) or "hi" (Hindi)
    """
    if language not in ["en", "hi"]:
        raise HTTPException(
            status_code=400,
            detail="Language must be 'en' (English) or 'hi' (Hindi)"
        )

    available_voices = kokoro_service.get_available_voices(language)

    return VoiceInfo(
        language=language,
        voice="af_bella" if language == "en" else "hi_maya",
        available_voices=available_voices
    )


@router.get("/voices/all")
async def get_all_voices() -> dict:
    """Get all available voices for all supported languages"""
    return {
        "en": kokoro_service.get_available_voices("en"),
        "hi": kokoro_service.get_available_voices("hi"),
    }
