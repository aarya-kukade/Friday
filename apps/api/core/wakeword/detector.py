"""
FRIDAY AI Operating System

Production Wake Word Detection Engine

Responsibilities
----------------
• Subscribe to AudioFrameEvent
• Run wake word inference
• Publish WakeWordDetectedEvent
• Manage listening state
"""

from __future__ import annotations

import threading
import time

from apps.api.core.eventbus import event_bus
from apps.api.core.events import (
    AudioFrameEvent,
    WakeWordDetectedEvent,
)

from apps.api.core.state.state_machine import state_machine
from apps.api.core.state.states import FridayState

from .config import wakeword_config
from .model import WakeWordModel


class WakeWordDetector:
    """
    Production Wake Word Detector.
    """

    def __init__(self):

        self.model = WakeWordModel(
            model_name=wakeword_config.model_name,
            model_path=wakeword_config.model_path,
            inference_framework=wakeword_config.inference_framework,
        )

        self._enabled = False

        self._lock = threading.RLock()

        self._last_detection = 0.0

        self._frames_processed = 0

        self._detections = 0

        self._last_confidence = 0.0

        self._cooldown = wakeword_config.debounce_time

    # =====================================================
    # Properties
    # =====================================================

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def frames_processed(self) -> int:
        return self._frames_processed

    @property
    def detections(self) -> int:
        return self._detections

    @property
    def last_confidence(self) -> float:
        return self._last_confidence

    # =====================================================
    # Lifecycle
    # =====================================================

    def start(self) -> None:
        """
        Starts wake word detection.
        """

        with self._lock:

            if self._enabled:
                return

            self._enabled = True

            event_bus.subscribe(
                AudioFrameEvent,
                self._on_audio_frame,
            )

            state_machine.transition(
                FridayState.WAKE_LISTENING
            )

            print("Wake Word Detector Started")

    def stop(self) -> None:
        """
        Stops wake word detection.
        """

        with self._lock:

            if not self._enabled:
                return

            self._enabled = False

            event_bus.unsubscribe(
                AudioFrameEvent,
                self._on_audio_frame,
            )

            print("Wake Word Detector Stopped")

        # =====================================================
    # Event Handling
    # =====================================================

    def _on_audio_frame(
        self,
        event: AudioFrameEvent,
    ) -> None:
        """
        Process one incoming audio frame.
        """

        if not self._enabled:
            return

        if not state_machine.is_state(
            FridayState.WAKE_LISTENING
        ):
            return

        if event.frame is None:
            return

        self._frames_processed += 1

        confidence = self.model.predict_with_patience(
            event.frame.samples,
            threshold=wakeword_config.threshold,
            patience=wakeword_config.patience,
        )

        self._last_confidence = confidence

        if confidence >= wakeword_config.threshold:
            self._trigger(confidence)

    # =====================================================
    # Wake Word Trigger
    # =====================================================

    def _trigger(
        self,
        confidence: float,
    ) -> None:
        """
        Called whenever the wake word has been detected.
        """

        now = time.monotonic()

        if now - self._last_detection < self._cooldown:
            return

        self._last_detection = now

        self._detections += 1

        print(
            f"Wake Word Detected ({confidence:.3f})"
        )

        state_machine.transition(
            FridayState.WAKE_DETECTED
        )

        event_bus.publish(
            WakeWordDetectedEvent(
                wake_word=wakeword_config.model_name,
                confidence=confidence,
            )
        )

    # =====================================================
    # Utilities
    # =====================================================

    def reset(self) -> None:
        """
        Reset detector statistics.
        """

        self.model.reset()

        self._frames_processed = 0
        self._detections = 0
        self._last_confidence = 0.0
        self._last_detection = 0.0

    def stats(self) -> dict:
        """
        Runtime statistics.
        """

        return {
            "enabled": self._enabled,
            "frames_processed": self._frames_processed,
            "detections": self._detections,
            "last_confidence": self._last_confidence,
            "cooldown": self._cooldown,
        }


# =====================================================
# Singleton
# =====================================================

wakeword_detector = WakeWordDetector()