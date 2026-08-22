"""
FRIDAY AI Operating System

Voice Activity Detection (VAD)

Detects whether an incoming AudioFrame contains speech.
Publishes SpeechStartedEvent and SpeechEndedEvent.
"""

from __future__ import annotations

import time
import threading
from collections import deque

import numpy as np

from apps.api.core.eventbus import event_bus
from apps.api.core.events import AudioFrameEvent, Event


class SpeechStartedEvent(Event):
    pass


class SpeechEndedEvent(Event):
    pass


class VoiceActivityDetector:

    def __init__(
        self,
        energy_threshold: float = 0.015,
        silence_timeout: float = 1.0,
        history_size: int = 10,
    ):

        self.energy_threshold = energy_threshold
        self.silence_timeout = silence_timeout

        self.history = deque(maxlen=history_size)

        self._speaking = False

        self._last_voice_time = 0.0

        self._lock = threading.RLock()

        self._frames_processed = 0

    @property
    def speaking(self):

        return self._speaking

    @property
    def frames_processed(self):

        return self._frames_processed

    def start(self):

        event_bus.subscribe(
            AudioFrameEvent,
            self._process_audio
        )

        print("Voice Activity Detector Started")

    def stop(self):

        event_bus.unsubscribe(
            AudioFrameEvent,
            self._process_audio
        )

        print("Voice Activity Detector Stopped")

    def _process_audio(self, event: AudioFrameEvent):

        if event.frame is None:
            return

        self._frames_processed += 1

        samples = event.frame.samples

        energy = self._calculate_rms(samples)

        self.history.append(energy)

        avg_energy = float(np.mean(self.history))

        current = time.monotonic()

        if avg_energy > self.energy_threshold:

            self._last_voice_time = current

            if not self._speaking:

                self._speaking = True

                event_bus.publish(
                    SpeechStartedEvent()
                )

        else:

            if (
                self._speaking
                and current - self._last_voice_time
                >= self.silence_timeout
            ):

                self._speaking = False

                event_bus.publish(
                    SpeechEndedEvent()
                )

    @staticmethod
    def _calculate_rms(samples: np.ndarray) -> float:

        if samples.size == 0:
            return 0.0

        return float(
            np.sqrt(
                np.mean(
                    np.square(samples)
                )
            )
        )

    def stats(self):

        return {

            "frames": self._frames_processed,

            "speaking": self._speaking,

            "average_energy": (
                float(np.mean(self.history))
                if self.history
                else 0.0
            ),
        }


vad = VoiceActivityDetector()