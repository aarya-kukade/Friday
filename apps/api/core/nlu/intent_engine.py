"""
FRIDAY AI Operating System

Natural Language Understanding Engine

Responsibilities
----------------
• Normalize transcripts
• Detect user intent
• Resolve aliases
• Extract entities
• Score confidence
• Produce Command objects
"""

from __future__ import annotations

import re
import string
from typing import Optional
from rapidfuzz import process
from apps.api.core.eventbus import event_bus
from apps.api.core.events import TranscriptReadyEvent

from apps.api.core.nlu.command import Command
from apps.api.core.nlu.aliases import APPLICATION_ALIASES
from apps.api.core.nlu.matcher import (
    OPEN_VERBS,
    CLOSE_VERBS,
    SEARCH_VERBS,
    CREATE_VERBS,
    DELETE_VERBS,
)


class IntentEngine:

    """
    Main Natural Language Understanding Engine.
    """

    def __init__(self):

        self.application_aliases = APPLICATION_ALIASES

        self.stop_words = {

            "please",
            "could",
            "would",
            "kindly",
            "can",
            "you",
            "me",
            "for",
            "the",
            "a",
            "an",
            "my",
            "to",
            "this",
            "that",
            "of",
            "on",
            "at",
            "with",

        }

        self.stats_data = {

            "processed": 0,

            "recognized": 0,

            "failed": 0,

        }

    # ----------------------------------------------------

    def start(self):

        event_bus.subscribe(

            TranscriptReadyEvent,

            self._handle_transcript,

        )

        print("Intent Engine Started")

    # ----------------------------------------------------

    def stop(self):

        event_bus.unsubscribe(

            TranscriptReadyEvent,

            self._handle_transcript,

        )

    # ----------------------------------------------------

    def _handle_transcript(

        self,

        event: TranscriptReadyEvent,

    ):

        command = self.parse(

            event.transcript,

            confidence=event.confidence,

        )

        if command is None:

            self.stats_data["failed"] += 1

            return

        self.stats_data["recognized"] += 1

        print(command)

        #
        # Event publication
        # Added in Part 3
        #

    # ----------------------------------------------------

    def parse(

        self,

        transcript: str,

        confidence: float = 1.0,

    ) -> Optional[Command]:

        self.stats_data["processed"] += 1

        text = self.normalize(transcript)

        tokens = self.tokenize(text)

        if not tokens:

            return None

        #
        # Intent Detection
        # Added Part 2
        #

        return None
    
        # ----------------------------------------------------

    def normalize(

        self,

        text: str,

    ) -> str:

        text = text.lower()

        text = text.strip()

        text = re.sub(

            r"\s+",

            " ",

            text,

        )

        text = text.translate(

            str.maketrans(

                "",

                "",

                string.punctuation,

            )

        )

        return text

    # ----------------------------------------------------

    def tokenize(

        self,

        text: str,

    ) -> list[str]:

        tokens = text.split()

        filtered = []

        for token in tokens:

            if token not in self.stop_words:

                filtered.append(token)

        return filtered
        # ----------------------------------------------------
        def resolve_application(
        self,
        text: str,
    ) -> Optional[str]:

          if text in self.application_aliases:
            return self.application_aliases[text]

        result = process.extractOne(
            text,
            self.application_aliases.keys(),
            score_cutoff=80,
        )

        if result:
            alias = result[0]
            return self.application_aliases[alias]

        return None

    # ----------------------------------------------------

    def contains_open_intent(
        self,
        tokens: list[str],
    ) -> bool:

        return any(
            token in OPEN_VERBS
            for token in tokens
        )

    # ----------------------------------------------------

def contains_close_intent(

        self,

        tokens: list[str],

    ) -> bool:

        return any(

            token in CLOSE_VERBS

            for token in tokens

        )

    # ----------------------------------------------------

def contains_search_intent(

        self,

        tokens: list[str],

    ) -> bool:

        return any(

            token in SEARCH_VERBS

            for token in tokens

        )

    # ----------------------------------------------------

def contains_create_intent(

        self,

        tokens: list[str],

    ) -> bool:

        return any(

            token in CREATE_VERBS

            for token in tokens

        )

    # ----------------------------------------------------

def contains_delete_intent(

        self,

        tokens: list[str],

    ) -> bool:

        return any(

            token in DELETE_VERBS

            for token in tokens

        )
    
        # ----------------------------------------------------

def stats(self):

        return dict(self.stats_data)


intent_engine = IntentEngine()

    # ----------------------------------------------------
    # Main Intent Parser
    # ----------------------------------------------------

def parse(
        self,
        transcript: str,
        confidence: float = 1.0,
    ) -> Optional[Command]:

        self.stats_data["processed"] += 1

        text = self.normalize(transcript)

        tokens = self.tokenize(text)

        if not tokens:
            return None

        #
        # OPEN
        #
        command = self._parse_open(text, tokens, confidence)

        if command:
            return command

        #
        # CLOSE
        #
        command = self._parse_close(text, tokens, confidence)

        if command:
            return command

        #
        # SEARCH
        #
        command = self._parse_search(text, tokens, confidence)

        if command:
            return command

        #
        # CREATE
        #
        command = self._parse_create(text, tokens, confidence)

        if command:
            return command

        #
        # DELETE
        #
        command = self._parse_delete(text, tokens, confidence)

        if command:
            return command

        return None

    # ----------------------------------------------------

        def _parse_open(
        self,
        text: str,
        tokens: list[str],
        confidence: float,
    ) -> Optional[Command]:

         if not self.contains_open_intent(tokens):
            return None

        app = self.resolve_application(text)

        if app:

            return Command(

                intent="open",

                target=app,

                arguments={},

                confidence=min(confidence, 0.98),

                original_text=text,

            )

        return None

    # ----------------------------------------------------

def _parse_close(
        self,
        text: str,
        tokens: list[str],
        confidence: float,
    ) -> Optional[Command]:

        if not self.contains_close_intent(tokens):
            return None

        app = self.resolve_application(text)

        if app:

            return Command(

                intent="close",

                target=app,

                arguments={},

                confidence=min(confidence, 0.96),

                original_text=text,

            )

        return None
       

           # ----------------------------------------------------

def _parse_search(
        self,
        text: str,
        tokens: list[str],
        confidence: float,
    ) -> Optional[Command]:

        if not self.contains_search_intent(tokens):
            return None

        query = text

        for verb in SEARCH_VERBS:

            query = query.replace(verb, "")

        query = query.strip()

        if not query:
            return None

        return Command(

            intent="search",

            target=query,

            arguments={},

            confidence=min(confidence, 0.95),

            original_text=text,

        )

    # ----------------------------------------------------

def _parse_create(
        self,
        text: str,
        tokens: list[str],
        confidence: float,
    ) -> Optional[Command]:

        if not self.contains_create_intent(tokens):
            return None

        filename = self.extract_filename(text)

        if filename:

            return Command(

                intent="create",

                target=filename,

                arguments={},

                confidence=min(confidence, 0.95),

                original_text=text,

            )

        return None
    # ----------------------------------------------------

def _parse_delete(
        self,
        text: str,
        tokens: list[str],
        confidence: float,
    ) -> Optional[Command]:

        if not self.contains_delete_intent(tokens):
            return None

        filename = self.extract_filename(text)

        if filename:

            return Command(

                intent="delete",

                target=filename,

                arguments={},

                confidence=min(confidence, 0.95),

                original_text=text,

            )

        return None
    # ----------------------------------------------------
def extract_filename(
        self,
        text: str,
    ) -> Optional[str]:

        pattern = r'[\w\-.]+\.[a-zA-Z0-9]+'

        match = re.search(pattern, text)

        if match:

            return match.group()

        return None