"""
Wake Word Configuration

Central configuration for the wake word engine.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class WakeWordConfig:

    model_name: str = "hey_jarvis"

    threshold: float = 0.55

    cooldown_seconds: float = 3.0

    confidence_window: int = 5

    sample_rate: int = 16000

    debug: bool = False


wakeword_config = WakeWordConfig()