"""
FRIDAY AI Operating System
==========================

Audio frame definitions used across the entire voice pipeline.

Every component (Wake Word, Whisper, Recorder, Visualizer)
receives immutable AudioFrame objects instead of raw numpy arrays.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

import numpy as np


@dataclass(slots=True, frozen=True)
class AudioFrame:
    """
    Represents one chunk of microphone audio.

    This object is immutable and safe to pass between
    threads and services.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    timestamp: datetime = field(default_factory=datetime.utcnow)

    samples: np.ndarray = field(default_factory=lambda: np.empty(0, dtype=np.float32))

    sample_rate: int = 16000

    channels: int = 1

    frame_index: int = 0

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> float:
        """Frame duration in seconds."""
        if self.sample_rate <= 0:
            return 0.0

        return len(self.samples) / self.sample_rate

    @property
    def sample_count(self) -> int:
        return len(self.samples)