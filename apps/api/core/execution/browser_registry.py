"""
Browser Registry

Stores supported browsers and their launch commands.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Browser:

    name: str

    executable: str


SUPPORTED_BROWSERS = {

    "chrome": Browser(
        "Google Chrome",
        "chrome.exe",
    ),

    "edge": Browser(
        "Microsoft Edge",
        "msedge.exe",
    ),

    "firefox": Browser(
        "Mozilla Firefox",
        "firefox.exe",
    ),

}