"""
FRIDAY AI Operating System

Speech Recorder

Responsibilities
----------------
• Start recording when speech starts
• Stop recording when speech ends
• Accumulate float32 audio frames
• Publish SpeechCapturedEvent
"""

from __future__ import annotations

import threading
from dataclasses import dataclass

import numpy as np

from apps.api.core.eventbus import event_bus
from apps.api.core.events import (
    Event,
    AudioFrameEvent,
)

from apps.api.core.voice.vad import (
    SpeechStartedEvent,
    SpeechEndedEvent,
)


# ==========================================================
# Event
# ==========================================================

@dataclass(slots=True)
class SpeechCapturedEvent(Event):
    """
    Fired when an entire speech segment
    has been recorded.
    """

    audio: np.ndarray | None = None

    sample_rate: int = 16000

    duration: float = 0.0


# ==========================================================
# Recorder
# ==========================================================

class SpeechRecorder:

    def __init__(self):

        self._recording = False

        self._lock = threading.RLock()

        self._frames: list[np.ndarray] = []

        self._sample_rate = 16000

        self._speech_count = 0

        self._total_audio_seconds = 0.0

    @property
    def recording(self):

        return self._recording

    def start(self):

        event_bus.subscribe(
            SpeechStartedEvent,
            self._on_speech_started,
        )

        event_bus.subscribe(
            SpeechEndedEvent,
            self._on_speech_ended,
        )

        event_bus.subscribe(
            AudioFrameEvent,
            self._on_audio_frame,
        )

        print("Speech Recorder Started")

    def stop(self):

        event_bus.unsubscribe(
            SpeechStartedEvent,
            self._on_speech_started,
        )

        event_bus.unsubscribe(
            SpeechEndedEvent,
            self._on_speech_ended,
        )

        event_bus.unsubscribe(
            AudioFrameEvent,
            self._on_audio_frame,
        )

        print("Speech Recorder Stopped")

    # ---------------------------------------------

    def _on_speech_started(self, event):

        with self._lock:

            self._frames.clear()

            self._recording = True

            print("Recording Started")

    # ---------------------------------------------

    def _on_audio_frame(self, event: AudioFrameEvent):

        if not self._recording:
            return

        if event.frame is None:
            return

        self._frames.append(
            event.frame.samples.copy()
        )

    # ---------------------------------------------

    def _on_speech_ended(self, event):

        with self._lock:

            if not self._recording:
                return

            self._recording = False

            if not self._frames:

                return

            audio = np.concatenate(
                self._frames,
                axis=0,
            )

            duration = (
                len(audio)
                / self._sample_rate
            )

            self._speech_count += 1

            self._total_audio_seconds += duration

            self._frames.clear()

            event_bus.publish(

                SpeechCapturedEvent(

                    audio=audio,

                    sample_rate=self._sample_rate,

                    duration=duration,

                )

            )

            print(
                f"Speech Recorded ({duration:.2f} sec)"
            )

    # ---------------------------------------------

    def reset(self):

        with self._lock:

            self._frames.clear()

            self._recording = False

    # ---------------------------------------------

    def stats(self):

        return {

            "recording": self._recording,

            "speech_segments": self._speech_count,

            "total_audio_seconds": round(

                self._total_audio_seconds,

                2,

            ),

        }


speech_recorder = SpeechRecorder()