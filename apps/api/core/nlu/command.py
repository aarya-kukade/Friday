"""
FRIDAY AI Operating System

Universal Command Object

Every subsystem after the NLU layer
uses this object.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Command:

    intent: str

    target: str | None = None

    arguments: dict[str, str] = field(default_factory=dict)

    confidence: float = 1.0

    original_text: str = ""

    source: str = "voice"