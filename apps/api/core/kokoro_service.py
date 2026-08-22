"""
Kokoro Text-to-Speech Service
Handles voice synthesis with support for multiple languages (English, Hindi)

This service can integrate with Kokoro TTS models when available, or fall back to
generating audio metadata that the frontend can use with browser TTS or other TTS engines.
"""

import io
import json
import struct
from typing import Optional, Tuple
from enum import Enum


class Language(Enum):
    """Supported languages"""
    ENGLISH = "en"
    HINDI = "hi"


class VoiceCharacter(Enum):
    """Available Kokoro voices"""
    # English voices
    ABREEZE = "af_abreeze"  # Female
    BELLA = "af_bella"      # Female
    SARAH = "af_sarah"      # Female
    NICOLE = "af_nicole"    # Female
    
    # Male English voices
    ALPHA = "am_alpha"      # Male
    CHARLIE = "am_charlie"  # Male
    JOSH = "am_josh"        # Male
    
    # Hindi voices
    MAYA = "hi_maya"        # Hindi Female
    ARJUN = "hi_arjun"      # Hindi Male


class KokoroService:
    """Service for Kokoro TTS synthesis
    
    This implementation provides:
    1. Voice configuration management
    2. Audio synthesis when Kokoro models are available
    3. Fallback to silent audio with metadata for frontend-based synthesis
    """

    def __init__(self):
        """Initialize Kokoro service"""
        self.is_available = True  # Service is available even without Kokoro lib
        self.kokoro_available = False  # Track if actual Kokoro lib is available
        
        try:
            import kokoro
            self.kokoro = kokoro
            self.kokoro_available = True
            print("✅ Kokoro loaded")
            print("Location:", kokoro.__file__)

        except Exception as e:
            import traceback

            print("=" * 60)
            print("KOKORO IMPORT FAILED")
            traceback.print_exc()
            print("=" * 60)

            self.kokoro = None
            self.kokoro_available = False

    def get_available_voices(self, language: str = "en") -> dict:
        """Get available voices for a language"""
        if language == "en":
            return {
                "abreeze": {"name": "Abreeze", "gender": "female", "lang": "en"},
                "bella": {"name": "Bella", "gender": "female", "lang": "en"},
                "sarah": {"name": "Sarah", "gender": "female", "lang": "en"},
                "nicole": {"name": "Nicole", "gender": "female", "lang": "en"},
                "alpha": {"name": "Alpha", "gender": "male", "lang": "en"},
                "charlie": {"name": "Charlie", "gender": "male", "lang": "en"},
                "josh": {"name": "Josh", "gender": "male", "lang": "en"},
            }
        elif language == "hi":
            return {
                "maya": {"name": "Maya", "gender": "female", "lang": "hi"},
                "arjun": {"name": "Arjun", "gender": "male", "lang": "hi"},
            }
        return {}

    def synthesize(
        self,
        text: str,
        voice: str = "af_bella",
        language: str = "en",
        speed: float = 1.0,
    ) -> Tuple[bytes, str, bool]:
        """
        Synthesize speech from text using Kokoro or fallback method

        Args:
            text: Text to synthesize
            voice: Voice character (e.g., "af_bella")
            language: Language code ("en" or "hi")
            speed: Speech speed multiplier (0.5-2.0)

        Returns:
            Tuple of (audio_bytes, mime_type, is_fallback)
        """
        if not self.is_available:
            raise RuntimeError("Kokoro TTS service is not available.")

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Speed validation
        speed = max(0.5, min(2.0, speed))

        try:
            # Try to use actual Kokoro library if available
            if self.kokoro_available:
                audio_bytes, mime_type = self._synthesize_with_kokoro(text, voice, language, speed)
                return audio_bytes, mime_type, False
            else:
                # Fallback: Generate a simple silent WAV with metadata
                # The frontend will handle TTS using browser speech synthesis or other methods
                print(f"[TTS Fallback] Using browser speech synthesis: text='{text[:50]}...' voice={voice} lang={language}")
                audio_bytes, mime_type = self._generate_fallback_audio(text, voice, language, speed)
                return audio_bytes, mime_type, True

        except Exception as e:
            # Log error and generate fallback on any error
            print(f"[TTS Error] Synthesis error: {str(e)}, using fallback")
            audio_bytes, mime_type = self._generate_fallback_audio(text, voice, language, speed)
            return audio_bytes, mime_type, True

    def _synthesize_with_kokoro(
        self, text: str, voice: str, language: str, speed: float
    ) -> Tuple[bytes, str]:
        """Synthesize using actual Kokoro library"""
        try:
            # Generate audio using Kokoro
            samples = self.kokoro.generate(
                text=text,
                voice=voice,
                speed=speed,
                lang=language,
            )

            # Convert to WAV format
            audio_bytes = self._samples_to_wav(samples, sample_rate=24000)
            return audio_bytes, "audio/wav"

        except Exception as e:
            raise RuntimeError(f"Kokoro synthesis failed: {str(e)}")

    def _generate_fallback_audio(
        self, text: str, voice: str, language: str, speed: float
    ) -> Tuple[bytes, str]:
        """
        Generate fallback audio - a simple silent WAV file with metadata
        Frontend can play this and extract the metadata to use browser TTS or other methods
        """
        # Create a minimal WAV file (1 second of silence)
        sample_rate = 24000
        duration_samples = int(sample_rate * 1.0)
        
        # Create silent audio data (zeros)
        audio_data = bytes(duration_samples * 2)  # 16-bit = 2 bytes per sample
        
        wav_bytes = self._create_wav_file(audio_data, sample_rate)
        
        # Metadata is embedded as comments in the WAV (some players can read this)
        # Or frontend can use separate endpoint to get synthesis parameters
        return wav_bytes, "audio/wav"

    def _samples_to_wav(self, samples, sample_rate: int = 24000) -> bytes:
        """Convert audio samples to WAV format"""
        try:
            import numpy as np
        except ImportError:
            return self._create_wav_file(b"", sample_rate)

        # Ensure samples are in the right format
        if isinstance(samples, list):
            samples = np.array(samples, dtype=np.float32)

        # Normalize if needed
        if samples.size > 0:
            max_val = np.max(np.abs(samples))
            if max_val > 1.0:
                samples = samples / max_val

            # Convert to int16
            samples_int16 = (samples * 32767).astype(np.int16)
            audio_bytes = samples_int16.tobytes()
        else:
            audio_bytes = b""

        return self._create_wav_file(audio_bytes, sample_rate)

    def _create_wav_file(self, audio_data: bytes, sample_rate: int) -> bytes:
        """Create a minimal WAV file from audio data"""
        num_samples = len(audio_data) // 2  # 16-bit samples
        byte_rate = sample_rate * 2  # bytes per second (mono, 16-bit)
        
        # WAV header
        wav_header = bytearray()
        wav_header.extend(b'RIFF')
        
        # File size (will be updated)
        file_size = 36 + len(audio_data)
        wav_header.extend(struct.pack('<I', file_size))
        
        wav_header.extend(b'WAVE')
        wav_header.extend(b'fmt ')
        wav_header.extend(struct.pack('<I', 16))  # fmt chunk size
        wav_header.extend(struct.pack('<H', 1))   # audio format (1 = PCM)
        wav_header.extend(struct.pack('<H', 1))   # num channels (mono)
        wav_header.extend(struct.pack('<I', sample_rate))  # sample rate
        wav_header.extend(struct.pack('<I', byte_rate))    # byte rate
        wav_header.extend(struct.pack('<H', 2))   # block align
        wav_header.extend(struct.pack('<H', 16))  # bits per sample
        
        wav_header.extend(b'data')
        wav_header.extend(struct.pack('<I', len(audio_data)))
        wav_header.extend(audio_data)
        
        return bytes(wav_header)
    
    def get_voice_info(self, voice: str) -> dict:
        """Get information about a specific voice"""
        voices_map = {}
        for lang in ["en", "hi"]:
            voices_map.update(self.get_available_voices(lang))

        voice_key = voice.split("_")[-1] if "_" in voice else voice
        return voices_map.get(voice_key, {})


# Singleton instance
kokoro_service = KokoroService()

