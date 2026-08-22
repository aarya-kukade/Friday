"""
FRIDAY AI Operating System

System Executor

Handles Windows system operations.
"""

from __future__ import annotations

import ctypes
import subprocess
from pathlib import Path

from apps.api.core.nlu.command import Command

from .base_executor import BaseExecutor


class SystemExecutor(BaseExecutor):

    def __init__(self):

        pass

    # ======================================================
    # Entry Point
    # ======================================================

    def execute(
        self,
        command: Command,
    ):

        match command.intent:

            case "system_lock":
                return self.lock()

            case "system_sleep":
                return self.sleep()

            case "system_restart":
                return self.restart()

            case "system_shutdown":
                return self.shutdown()

            case "system_logoff":
                return self.logoff()

            case "system_settings":
                return self.settings()

            case "system_task_manager":
                return self.task_manager()

            case "system_control_panel":
                return self.control_panel()

            case "system_explorer":
                return self.explorer()

            case "system_recycle_bin":
                return self.recycle_bin()

            case _:
                return False

    # ======================================================
    # Windows
    # ======================================================

    def lock(self):

        ctypes.windll.user32.LockWorkStation()

        return True

    # ------------------------------------------------------

    def sleep(self):

        subprocess.run(

            [
                "rundll32.exe",
                "powrprof.dll,SetSuspendState",
                "0,1,0",
            ]

        )

        return True

    # ------------------------------------------------------

    def shutdown(self):

        subprocess.run(

            [
                "shutdown",
                "/s",
                "/t",
                "0",
            ]

        )

        return True

    # ------------------------------------------------------

    def restart(self):

        subprocess.run(

            [
                "shutdown",
                "/r",
                "/t",
                "0",
            ]

        )

        return True

    # ------------------------------------------------------

    def logoff(self):

        subprocess.run(

            [
                "shutdown",
                "/l",
            ]

        )

        return True

    # ======================================================
    # Windows Apps
    # ======================================================

    def settings(self):

        subprocess.Popen(

            [
                "start",
                "ms-settings:",
            ],

            shell=True,

        )

        return True

    # ------------------------------------------------------

    def task_manager(self):

        subprocess.Popen(

            [
                "taskmgr",
            ]

        )

        return True

    # ------------------------------------------------------

    def control_panel(self):

        subprocess.Popen(

            [
                "control",
            ]

        )

        return True

    # ------------------------------------------------------

    def explorer(self):

        subprocess.Popen(

            [
                "explorer",
            ]

        )

        return True

    # ------------------------------------------------------

    def recycle_bin(self):

        subprocess.Popen(

            [
                "explorer.exe",
                "shell:RecycleBinFolder",
            ]

        )

        return True


system_executor = SystemExecutor()