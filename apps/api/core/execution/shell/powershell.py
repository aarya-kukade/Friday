"""
FRIDAY AI Operating System

PowerShell Interface
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .shell import shell, ShellResult


class PowerShell:

    def __init__(self):

        self.executable = "powershell.exe"

    # ----------------------------------------------------------

    def run(
        self,
        command: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        ps_command = f'{self.executable} -NoProfile -ExecutionPolicy Bypass -Command "{command}"'

        return shell.run(
            command=ps_command,
            cwd=cwd,
        )

    # ----------------------------------------------------------

    def script(
        self,
        script_path: str | Path,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        script_path = Path(script_path).resolve()

        command = (
            f'{self.executable} '
            f'-ExecutionPolicy Bypass '
            f'-File "{script_path}"'
        )

        return shell.run(
            command=command,
            cwd=cwd,
        )

    # ----------------------------------------------------------

    def get_processes(self):

        return self.run("Get-Process")

    # ----------------------------------------------------------

    def get_services(self):

        return self.run("Get-Service")

    # ----------------------------------------------------------

    def stop_process(self, process_name: str):

        return self.run(

            f'Stop-Process -Name "{process_name}" -Force'

        )

    # ----------------------------------------------------------

    def start_process(self, executable: str):

        return self.run(

            f'Start-Process "{executable}"'

        )

    # ----------------------------------------------------------

    def install_winget_package(self, package: str):

        return self.run(

            f'winget install "{package}"'

        )

    # ----------------------------------------------------------

    def current_execution_policy(self):

        return self.run(

            "Get-ExecutionPolicy"

        )


powershell = PowerShell()