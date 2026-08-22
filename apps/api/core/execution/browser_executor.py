"""
Browser Executor

Handles browser related commands.
"""

from __future__ import annotations

import subprocess
import urllib.parse

from apps.api.core.nlu.command import Command

from .base_executor import BaseExecutor
from .browser_registry import SUPPORTED_BROWSERS


class BrowserExecutor(BaseExecutor):

    def __init__(self):

        self.default_browser = "edge"

    # ---------------------------------------------------------

    def execute(self, command: Command):

        if command.intent == "search":

            return self.search(command.target)

        if command.intent == "open_url":

            return self.open_url(command.target)

        return False

    # ---------------------------------------------------------

    def search(self, query: str):

        browser = SUPPORTED_BROWSERS[self.default_browser]

        encoded = urllib.parse.quote_plus(query)

        url = f"https://www.bing.com/search?q={encoded}"

        subprocess.Popen(

            [

                browser.executable,

                url,

            ]

        )

        return True

    # ---------------------------------------------------------

    def open_url(self, url: str):

        browser = SUPPORTED_BROWSERS[self.default_browser]

        subprocess.Popen(

            [

                browser.executable,

                url,

            ]

        )

        return True


browser_executor = BrowserExecutor()