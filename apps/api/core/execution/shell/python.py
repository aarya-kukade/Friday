"""
FRIDAY AI Operating System

Python Shell Interface

Provides high-level Python development operations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .shell import shell, ShellResult


class PythonShell:

    def __init__(self):

        self.python = "python"

    # ----------------------------------------------------------
    # Core
    # ----------------------------------------------------------

    def run(
        self,
        command: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return shell.run(
            f"{self.python} {command}",
            cwd=cwd,
        )

    # ----------------------------------------------------------
    # Execute Script
    # ----------------------------------------------------------

    def script(
        self,
        script: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'"{script}"',
            cwd,
        )

    # ----------------------------------------------------------
    # Execute Module
    # ----------------------------------------------------------

    def module(
        self,
        module: str,
        arguments: str = "",
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'-m {module} {arguments}',
            cwd,
        )

    # ----------------------------------------------------------
    # Pip
    # ----------------------------------------------------------

    def pip_install(
        self,
        package: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'-m pip install {package}',
            cwd,
        )

    def pip_uninstall(
        self,
        package: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'-m pip uninstall -y {package}',
            cwd,
        )

    def pip_upgrade(
        self,
        package: str,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'-m pip install --upgrade {package}',
            cwd,
        )

    def pip_freeze(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            "-m pip freeze",
            cwd,
        )

    # ----------------------------------------------------------
    # Virtual Environment
    # ----------------------------------------------------------

    def create_venv(
        self,
        name: str = ".venv",
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'-m venv "{name}"',
            cwd,
        )

    # ----------------------------------------------------------
    # Requirements
    # ----------------------------------------------------------

    def install_requirements(
        self,
        file: str = "requirements.txt",
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return self.run(
            f'-m pip install -r "{file}"',
            cwd,
        )

    def generate_requirements(
        self,
        file: str = "requirements.txt",
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        command = f'{self.python} -m pip freeze > "{file}"'

        return shell.run(
            command,
            cwd=cwd,
        )

    # ----------------------------------------------------------
    # Uvicorn
    # ----------------------------------------------------------

    def uvicorn(
        self,
        app: str,
        reload: bool = True,
        host: str = "127.0.0.1",
        port: int = 8000,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        command = (
            f'-m uvicorn {app} '
            f'--host {host} '
            f'--port {port}'
        )

        if reload:
            command += " --reload"

        return self.run(
            command,
            cwd,
        )

    # ----------------------------------------------------------
    # Version
    # ----------------------------------------------------------

    def version(self) -> ShellResult:

        return shell.run(
            "python --version"
        )

    # ----------------------------------------------------------
    # Interactive
    # ----------------------------------------------------------

    def repl(
        self,
        cwd: Optional[str | Path] = None,
    ) -> ShellResult:

        return shell.run(
            "python",
            cwd,
        )


python_shell = PythonShell()