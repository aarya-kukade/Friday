"""
FRIDAY AI Operating System

Transcript Processor

Converts natural language into structured commands.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from apps.api.core.eventbus import event_bus
from apps.api.core.events import (
    TranscriptReadyEvent,
    Event,
)


# ============================================================
# EVENT
# ============================================================

@dataclass(slots=True)
class IntentReadyEvent(Event):

    intent: str

    target: str

    original_text: str

    confidence: float


# ============================================================
# COMMAND
# ============================================================

@dataclass(slots=True)
class Command:

    intent: str

    target: str

    arguments: list[str]

    confidence: float


# ============================================================
# PROCESSOR
# ============================================================

class TranscriptProcessor:

    def __init__(self):

        self._applications = {

            "vs code": "code",

            "visual studio code": "code",

            "chrome": "chrome",

            "google chrome": "chrome",

            "edge": "msedge",

            "firefox": "firefox",

            "calculator": "calc",

            "paint": "mspaint",

            "notepad": "notepad",

            "terminal": "cmd",

            "command prompt": "cmd",

            "powershell": "powershell",

            "explorer": "explorer",

        }

    # --------------------------------------------------------

    def start(self):

        event_bus.subscribe(

            TranscriptReadyEvent,

            self._process,

        )

        print("Transcript Processor Started")

    # --------------------------------------------------------

    def stop(self):

        event_bus.unsubscribe(

            TranscriptReadyEvent,

            self._process,

        )

    # --------------------------------------------------------

    def _process(

        self,

        event: TranscriptReadyEvent,

    ):

        text = event.transcript.lower().strip()

        command = self.parse(text)

        if command is None:

            return

        event_bus.publish(

            IntentReadyEvent(

                intent=command.intent,

                target=command.target,

                original_text=text,

                confidence=command.confidence,

            )

        )

    # --------------------------------------------------------

    def parse(

        self,

        text: str,

    ) -> Optional[Command]:

        # OPEN

        if text.startswith("open"):

            target = text.replace(

                "open",

                "",

                1,

            ).strip()

            target = self._applications.get(

                target,

                target,

            )

            return Command(

                intent="open",

                target=target,

                arguments=[],

                confidence=0.95,

            )

        # CLOSE

        if text.startswith("close"):

            target = text.replace(

                "close",

                "",

                1,

            ).strip()

            return Command(

                intent="close",

                target=target,

                arguments=[],

                confidence=0.94,

            )

        # SEARCH

        if text.startswith("search"):

            query = text.replace(

                "search",

                "",

                1,

            ).strip()

            return Command(

                intent="search",

                target=query,

                arguments=[],

                confidence=0.92,

            )

        return None


transcript_processor = TranscriptProcessor()