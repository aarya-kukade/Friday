"""
FRIDAY AI Operating System

Git Shell Interface

Provides high-level Git operations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .shell import shell, ShellResult


class GitShell:

    def __init__(self):

        self.git = "git"

    # ----------------------------------------------------------
    # Core Runner
    # ----------------------------------------------------------

    def run(
        self,
        command: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return shell.run(
            f"{self.git} {command}",
            cwd=cwd,
        )

    # ----------------------------------------------------------
    # Repository Information
    # ----------------------------------------------------------

    def status(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run("status", cwd)

    def log(
        self,
        count: int = 10,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f"log --oneline -n {count}",
            cwd,
        )

    def branch(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run("branch", cwd)

    def current_branch(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            "branch --show-current",
            cwd,
        )

    # ----------------------------------------------------------
    # Repository Management
    # ----------------------------------------------------------

    def init(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run("init", cwd)

    def clone(
        self,
        repository: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'clone "{repository}"',
            cwd,
        )

    # ----------------------------------------------------------
    # Staging
    # ----------------------------------------------------------

    def add(
        self,
        target: str = ".",
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'add "{target}"',
            cwd,
        )

    def restore(
        self,
        target: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'restore "{target}"',
            cwd,
        )

    # ----------------------------------------------------------
    # Commit
    # ----------------------------------------------------------

    def commit(
        self,
        message: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'commit -m "{message}"',
            cwd,
        )

    # ----------------------------------------------------------
    # Remote
    # ----------------------------------------------------------

    def pull(
        self,
        remote: str = "origin",
        branch: str = "main",
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f"pull {remote} {branch}",
            cwd,
        )

    def push(
        self,
        remote: str = "origin",
        branch: str = "main",
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f"push {remote} {branch}",
            cwd,
        )

    def fetch(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run("fetch", cwd)

    # ----------------------------------------------------------
    # Branch Management
    # ----------------------------------------------------------

    def checkout(
        self,
        branch: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'checkout "{branch}"',
            cwd,
        )

    def create_branch(
        self,
        branch: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'checkout -b "{branch}"',
            cwd,
        )

    def merge(
        self,
        branch: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'merge "{branch}"',
            cwd,
        )


git_shell = GitShell()