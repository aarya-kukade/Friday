"""
FRIDAY AI Operating System

Whisper Speech-To-Text Service

Responsibilities
----------------
• Subscribe to SpeechCapturedEvent
• Run Faster-Whisper locally
• Publish TranscriptReadyEvent
"""

from __future__ import annotations

import threading
from dataclasses import dataclass

import numpy as np
from faster_whisper import WhisperModel

from apps.api.core.eventbus import event_bus
from apps.api.core.events import (
    Event,
    SpeechCapturedEvent,
)


# ============================================================
# EVENT
# ============================================================

@dataclass(slots=True)
class TranscriptReadyEvent(Event):

    transcript: str = ""

    language: str = "en"

    confidence: float = 0.0


# ============================================================
# SERVICE
# ============================================================

class WhisperService:

    def __init__(

        self,

        model_size: str = "base",

        device: str = "cpu",

        compute_type: str = "int8",

    ):

        self.model_size = model_size

        self.device = device

        self.compute_type = compute_type

        self._lock = threading.RLock()

        self.model = WhisperModel(

            model_size,

            device=device,

            compute_type=compute_type,

        )

        self._transcriptions = 0

    # --------------------------------------------------------

    def start(self):

        event_bus.subscribe(

            SpeechCapturedEvent,

            self._transcribe,

        )

        print("Whisper Service Started")

    # --------------------------------------------------------

    def stop(self):

        event_bus.unsubscribe(

            SpeechCapturedEvent,

            self._transcribe,

        )

        print("Whisper Service Stopped")

    # --------------------------------------------------------

    def _transcribe(

        self,

        event: SpeechCapturedEvent,

    ):

        if event.audio is None:

            return

        with self._lock:

            segments, info = self.model.transcribe(

                event.audio,

                beam_size=5,

                vad_filter=True,

            )

            transcript = ""

            confidence = 0.0

            count = 0

            for segment in segments:

                transcript += segment.text + " "

                confidence += segment.avg_logprob

                count += 1

            transcript = transcript.strip()

            if count > 0:

                confidence /= count

            self._transcriptions += 1

            print("Transcript:", transcript)

            event_bus.publish(

                TranscriptReadyEvent(

                    transcript=transcript,

                    language=info.language,

                    confidence=confidence,

                )

            )

    # --------------------------------------------------------

    def stats(self):

        return {

            "model": self.model_size,

            "device": self.device,

            "transcriptions": self._transcriptions,

        }


whisper_service = WhisperService()