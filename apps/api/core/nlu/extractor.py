"""
Entity Extraction Utilities
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


FILE_PATTERN = re.compile(
    r'[\w\-. ]+\.(txt|pdf|doc|docx|ppt|pptx|xlsx|csv|json|py|js|ts|html|css|md)',
    re.IGNORECASE,
)

URL_PATTERN = re.compile(
    r'https?://[^\s]+',
    re.IGNORECASE,
)

WINDOWS_PATH_PATTERN = re.compile(
    r'[A-Za-z]:\\(?:[^<>:"/\\|?*\n]+\\?)*'
)

NUMBER_PATTERN = re.compile(r"\b\d+\b")


class EntityExtractor:

    @staticmethod
    def extract_filename(text: str) -> Optional[str]:

        match = FILE_PATTERN.search(text)

        return match.group(0) if match else None

    @staticmethod
    def extract_url(text: str) -> Optional[str]:

        match = URL_PATTERN.search(text)

        return match.group(0) if match else None

    @staticmethod
    def extract_path(text: str) -> Optional[str]:

        match = WINDOWS_PATH_PATTERN.search(text)

        return match.group(0) if match else None

    @staticmethod
    def extract_number(text: str) -> Optional[int]:

        match = NUMBER_PATTERN.search(text)

        if match:

            return int(match.group())

        return None

    @staticmethod
    def looks_like_folder(text: str) -> bool:

        p = Path(text)

        return "." not in p.name