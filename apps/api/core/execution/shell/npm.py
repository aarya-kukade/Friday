"""
FRIDAY AI Operating System

NPM Shell Interface

Provides high-level Node.js and npm operations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .shell import shell, ShellResult


class NPMShell:

    def __init__(self):

        self.npm = "npm"

        self.npx = "npx"

    # ----------------------------------------------------------
    # Core Runner
    # ----------------------------------------------------------

    def run(
        self,
        command: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return shell.run(
            f"{self.npm} {command}",
            cwd=cwd,
        )

    # ----------------------------------------------------------
    # Package Management
    # ----------------------------------------------------------

    def install(
        self,
        package: Optional[str] = None,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        if package:

            return self.run(
                f'install "{package}"',
                cwd,
            )

        return self.run(
            "install",
            cwd,
        )

    def uninstall(
        self,
        package: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'uninstall "{package}"',
            cwd,
        )

    def update(
        self,
        package: Optional[str] = None,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        if package:

            return self.run(
                f'update "{package}"',
                cwd,
            )

        return self.run(
            "update",
            cwd,
        )

    # ----------------------------------------------------------
    # Project Commands
    # ----------------------------------------------------------

    def start(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            "start",
            cwd,
        )

    def dev(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            "run dev",
            cwd,
        )

    def build(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            "run build",
            cwd,
        )

    def test(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            "test",
            cwd,
        )

    # ----------------------------------------------------------
    # Package Information
    # ----------------------------------------------------------

    def list(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            "list",
            cwd,
        )

    def outdated(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            "outdated",
            cwd,
        )

    def audit(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            "audit",
            cwd,
        )

    # ----------------------------------------------------------
    # NPX
    # ----------------------------------------------------------

    def npx_run(
        self,
        command: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return shell.run(
            f"{self.npx} {command}",
            cwd=cwd,
        )

    # ----------------------------------------------------------
    # Version
    # ----------------------------------------------------------

    def version(self) -> ShellResult:

        return self.run(
            "--version",
        )


npm_shell = NPMShell()