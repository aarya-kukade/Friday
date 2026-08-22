"""
Application Executor

Handles opening and closing desktop applications.
"""

from __future__ import annotations

import os
import subprocess
import psutil

from apps.api.core.nlu.command import Command

from .base_executor import BaseExecutor


class AppExecutor(BaseExecutor):

    def __init__(self):

        self.apps = {

            "code": "Code.exe",

            "chrome": "chrome.exe",

            "firefox": "firefox.exe",

            "msedge": "msedge.exe",

            "notepad": "notepad.exe",

            "calc": "calc.exe",

            "mspaint": "mspaint.exe",

            "cmd": "cmd.exe",

            "powershell": "powershell.exe",

            "explorer": "explorer.exe",

        }

    # --------------------------------------------------------

    def execute(self, command: Command):

        if command.intent == "open":

            return self.open(command.target)

        if command.intent == "close":

            return self.close(command.target)

        return False

    # --------------------------------------------------------

    def open(self, app: str):

        if app not in self.apps:

            print(f"Unknown application: {app}")

            return False

        executable = self.apps[app]

        try:

            if executable == "explorer.exe":

                subprocess.Popen(["explorer"])

            elif executable == "calc.exe":

                subprocess.Popen(["calc"])

            else:

                subprocess.Popen([executable])

            print(f"Opened {app}")

            return True

        except Exception as e:

            print(e)

            return False

    # --------------------------------------------------------

    def close(self, app: str):

        if app not in self.apps:

            return False

        executable = self.apps[app].lower()

        killed = False

        for process in psutil.process_iter(["name"]):

            try:

                if process.info["name"] and process.info["name"].lower() == executable:

                    process.kill()

                    killed = True

            except Exception:

                pass

        return killed


app_executor = AppExecutor()