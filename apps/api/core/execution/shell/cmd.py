"""
FRIDAY AI Operating System

Command Prompt Interface

Provides structured access to Windows CMD commands.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .shell import shell, ShellResult


class CommandPrompt:

    def __init__(self):

        self.executable = "cmd.exe"

    # ----------------------------------------------------------
    # Core Command Runner
    # ----------------------------------------------------------

    def run(
        self,
        command: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        cmd_command = f'{self.executable} /C "{command}"'

        return shell.run(
            command=cmd_command,
            cwd=cwd,
        )

    # ----------------------------------------------------------
    # Directory Operations
    # ----------------------------------------------------------

    def dir(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run("dir", cwd)

    def tree(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run("tree", cwd)

    def mkdir(
        self,
        folder: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(f'mkdir "{folder}"', cwd)

    def rmdir(
        self,
        folder: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(f'rmdir /S /Q "{folder}"', cwd)

    def cd(
        self,
        folder: str,
    ) -> bool:

        return shell.change_directory(folder)

    def pwd(self) -> str:

        return shell.current_directory()

    # ----------------------------------------------------------
    # File Operations
    # ----------------------------------------------------------

    def copy(
        self,
        source: str,
        destination: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'copy "{source}" "{destination}"',
            cwd,
        )

    def move(
        self,
        source: str,
        destination: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'move "{source}" "{destination}"',
            cwd,
        )

    def delete(
        self,
        target: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'del /F /Q "{target}"',
            cwd,
        )

    def rename(
        self,
        source: str,
        destination: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'ren "{source}" "{destination}"',
            cwd,
        )

    # ----------------------------------------------------------
    # Utilities
    # ----------------------------------------------------------

    def cls(self) -> ShellResult:

        return self.run("cls")

    def echo(
        self,
        text: str,
    ) -> ShellResult:

        return self.run(f'echo {text}')

    def start(
        self,
        target: str,
    ) -> ShellResult:

        return self.run(f'start "" "{target}"')

    def where(
        self,
        executable: str,
    ) -> ShellResult:

        return self.run(f'where {executable}')

    def tasklist(self) -> ShellResult:

        return self.run("tasklist")

    def taskkill(
        self,
        process: str,
    ) -> ShellResult:

        return self.run(

            f'taskkill /F /IM "{process}"'

        )


cmd = CommandPrompt()