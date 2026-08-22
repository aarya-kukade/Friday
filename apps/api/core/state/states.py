"""
FRIDAY AI Operating System

State definitions for the FRIDAY kernel.

Only one state may be active at a time.
"""

from __future__ import annotations

from enum import Enum


class FridayState(str, Enum):
    """Represents every possible operating state of FRIDAY."""

    BOOTING = "BOOTING"

    INITIALIZING = "INITIALIZING"

    READY = "READY"

    WAKE_LISTENING = "WAKE_LISTENING"

    WAKE_DETECTED = "WAKE_DETECTED"

    COMMAND_LISTENING = "COMMAND_LISTENING"

    TRANSCRIBING = "TRANSCRIBING"

    THINKING = "THINKING"

    EXECUTING = "EXECUTING"

    GENERATING_RESPONSE = "GENERATING_RESPONSE"

    SPEAKING = "SPEAKING"

    IDLE = "IDLE"

    ERROR = "ERROR"

    SHUTDOWN = "SHUTDOWN"