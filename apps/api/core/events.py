"""
FRIDAY AI Operating System
Core Event Definitions

Every subsystem communicates by publishing and subscribing
to strongly typed events.

Author: FRIDAY Core
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from apps.api.core.audio.audio_stream import AudioFrame


# ==========================================================
# Base Event
# ==========================================================

@dataclass(slots=True)
class Event:
    """
    Base event class.
    """

    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ==========================================================
# Audio Events
# ==========================================================

@dataclass(slots=True)
class AudioFrameEvent(Event):

    frame: AudioFrame | None = None


# ==========================================================
# Wake Word Events
# ==========================================================

@dataclass(slots=True)
class WakeWordDetectedEvent(Event):

    wake_word: str = "friday"

    confidence: float = 0.0


# ==========================================================
# Speech Events
# ==========================================================

@dataclass(slots=True)
class ListeningStartedEvent(Event):
    pass


@dataclass(slots=True)
class ListeningStoppedEvent(Event):
    pass


@dataclass(slots=True)
class TranscriptReadyEvent(Event):

    transcript: str = ""


# ==========================================================
# AI Events
# ==========================================================

@dataclass(slots=True)
class IntentDetectedEvent(Event):

    intent: str = ""


@dataclass(slots=True)
class ResponseReadyEvent(Event):

    response: str = ""


# ==========================================================
# Execution Events
# ==========================================================

@dataclass(slots=True)
class ExecutionStartedEvent(Event):

    command: str = ""


@dataclass(slots=True)
class ExecutionCompletedEvent(Event):

    success: bool = True

    message: str = ""


# ==========================================================
# Voice Events
# ==========================================================

@dataclass(slots=True)
class SpeakingStartedEvent(Event):
    pass


@dataclass(slots=True)
class SpeakingFinishedEvent(Event):
    pass


# ==========================================================
# System Events
# ==========================================================

@dataclass(slots=True)
class ShutdownEvent(Event):
    pass
