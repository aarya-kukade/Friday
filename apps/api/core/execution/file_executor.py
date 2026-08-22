"""
FRIDAY AI Operating System

File Executor

Handles local file and folder operations.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from apps.api.core.execution import registry
from apps.api.core.nlu.command import Command
from .base_executor import BaseExecutor


class FileExecutor(BaseExecutor):

    def __init__(self):

        self.workspace = Path.home()

    # --------------------------------------------------

    def execute(self, command: Command):

        match command.intent:

            case "create":
                return self.create(command)

            case "delete":
                return self.delete(command)

            case "rename":
                return self.rename(command)

            case "move":
                return self.move(command)

            case "copy":
                return self.copy(command)
            
            case "write":
                return self.write(command)

            case "read":
                return self.read(command)

            case "open_folder":
                return self.open_folder(command)

            case _:
                return False
            
                # --------------------------------------------------

    def resolve(self, target: str) -> Path:

        path = Path(target)

        if path.is_absolute():

            return path

        return self.workspace / path

            # --------------------------------------------------

    def create(self, command: Command):

        path = self.resolve(command.target)

        path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        path.touch(

            exist_ok=True,

        )

        print(f"Created {path}")

        return True
    
        # --------------------------------------------------

    def delete(self, command: Command):

        path = self.resolve(command.target)

        if not path.exists():

            return False

        if path.is_file():

            path.unlink()

        else:

            shutil.rmtree(path)

        print(f"Deleted {path}")

        return True
    
        # --------------------------------------------------

    def rename(self, command: Command):

        source = self.resolve(command.arguments["source"])

        target = self.resolve(command.arguments["target"])

        source.rename(target)

        print(

            f"Renamed {source} -> {target}"

        )

        return True
    
        # --------------------------------------------------

    def move(self, command: Command):

        source = self.resolve(command.arguments["source"])

        destination = self.resolve(command.arguments["destination"])

        shutil.move(

            source,

            destination,

        )

        return True
    
        # --------------------------------------------------

    def copy(self, command: Command):

        source = self.resolve(command.arguments["source"])

        destination = self.resolve(command.arguments["destination"])

        shutil.copy2(

            source,

            destination,

        )

        return True


            # --------------------------------------------------

    def read(self, command: Command):

        path = self.resolve(command.target)

        if not path.exists():

            return None

        return path.read_text(

            encoding="utf-8",

        )
    
        # --------------------------------------------------

    def open_folder(self, command: Command):

        import subprocess

        folder = self.resolve(command.target)

        subprocess.Popen(

            [

                "explorer",

                str(folder),

            ]

        )

        return True

    # --------------------------------------------------
    # Write File
    # --------------------------------------------------

    def write(self, command: Command):

        path = self.resolve(command.target)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        content = command.arguments.get(
            "content",
            "",
        )

        append = command.arguments.get(
            "append",
            False,
        )

        encoding = command.arguments.get(
            "encoding",
            "utf-8",
        )

        mode = "a" if append else "w"

        with open(
            path,
            mode,
            encoding=encoding,
        ) as file:

            file.write(content)

        print(f"Written to {path}")

        return True

file_executor = FileExecutor()

registry.register(
    
    "write",

    file_executor.write,
)

registry.register(

    "create",

    file_executor.create,

)

registry.register(

    "delete",

    file_executor.delete,

)

registry.register(

    "rename",

    file_executor.rename,

)

registry.register(

    "move",

    file_executor.move,

)

registry.register(

    "copy",

    file_executor.copy,

)

registry.register(

    "read",

    file_executor.read,

)

registry.register(

    "open_folder",

    file_executor.open_folder,

)