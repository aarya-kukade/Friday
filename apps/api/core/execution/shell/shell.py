"""
FRIDAY AI Operating System

Base Shell Runner

Responsibilities
----------------
- Execute shell commands
- Capture stdout / stderr
- Timeout handling
- Working directory support
- Environment variable support
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ==========================================================
# Result Object
# ==========================================================

@dataclass(slots=True)
class ShellResult:

    success: bool

    command: str

    return_code: int

    stdout: str

    stderr: str

    working_directory: str


# ==========================================================
# Base Shell
# ==========================================================

class Shell:

    def __init__(self):

        self.default_timeout = 300

        self.default_cwd = Path.cwd()

    # ------------------------------------------------------

    def run(

        self,

        command: str,

        cwd: Optional[str | Path] = None,

        timeout: Optional[int] = None,

        shell: bool = True,

        env: Optional[dict] = None,

    ) -> ShellResult:

        working_directory = Path(cwd) if cwd else self.default_cwd

        timeout = timeout or self.default_timeout

        merged_env = os.environ.copy()

        if env:

            merged_env.update(env)

        try:

            process = subprocess.run(

                command,

                shell=shell,

                cwd=working_directory,

                env=merged_env,

                capture_output=True,

                text=True,

                timeout=timeout,

            )

            return ShellResult(

                success=process.returncode == 0,

                command=command,

                return_code=process.returncode,

                stdout=process.stdout.strip(),

                stderr=process.stderr.strip(),

                working_directory=str(working_directory),

            )

        except subprocess.TimeoutExpired:

            return ShellResult(

                success=False,

                command=command,

                return_code=-1,

                stdout="",

                stderr="Command timed out.",

                working_directory=str(working_directory),

            )

        except Exception as e:

            return ShellResult(

                success=False,

                command=command,

                return_code=-1,

                stdout="",

                stderr=str(e),

                working_directory=str(working_directory),

            )

    # ------------------------------------------------------

    def exists(

        self,

        path: str | Path,

    ) -> bool:

        return Path(path).exists()

    # ------------------------------------------------------

    def change_directory(

        self,

        directory: str | Path,

    ) -> bool:

        directory = Path(directory)

        if directory.exists():

            self.default_cwd = directory.resolve()

            return True

        return False

    # ------------------------------------------------------

    def current_directory(self) -> str:

        return str(self.default_cwd)

    # ------------------------------------------------------

    def reset(self):

        self.default_cwd = Path.cwd()


shell = Shell()