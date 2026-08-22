import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class FileOperationHandler:
    """Handles local file system operations inside the project workspace."""

    def __init__(self, base_path: str | None = None):
        project_root = Path(__file__).resolve().parents[3]
        if base_path is None:
            candidates = []
            env_path = os.environ.get("FRIDAY_WORKSPACE_PATH")
            if env_path:
                candidates.append(Path(env_path).expanduser())
            candidates.extend([project_root / "workspace", project_root / "apps" / "api"])
            for candidate in candidates:
                if candidate.exists():
                    base_path = str(candidate)
                    break
            else:
                base_path = str(project_root / "workspace")

        self.base_path = Path(base_path).expanduser().resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.app_aliases = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "command prompt": "cmd.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "vscode": "code.exe",
            "idle":"idle.pyw",
            "python": "idle.pyw",
        }

    def _validate_path(self, file_path: str) -> Path:
        if not file_path:
            return self.base_path

        candidate = Path(file_path).expanduser()
        if not candidate.is_absolute():
            candidate = self.base_path / candidate

        candidate = candidate.resolve()
        try:
            candidate.relative_to(self.base_path.resolve())
        except ValueError as exc:
            raise ValueError(f"Access denied: {file_path}") from exc

        return candidate

    def create_file(self, file_path: str, content: str = "") -> Dict[str, Any]:
        try:
            target_path = self._validate_path(file_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)

            if target_path.exists():
                print(f"[FileOperations] File already exists: {file_path}")
                return {
                    "status": "error",
                    "message": f"File already exists: {file_path}",
                    "file_path": file_path,
                }

            target_path.write_text(content, encoding="utf-8")
            print(f"[FileOperations] File created successfully: {file_path}")
            return {
                "status": "success",
                "message": f"File created: {file_path}",
                "file_path": file_path,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            error_msg = str(e)
            print(f"[FileOperations] Error creating file: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "file_path": file_path,
            }

    def read_file(self, file_path: str) -> Dict[str, Any]:
        try:
            target_path = self._validate_path(file_path)

            if not target_path.exists():
                print(f"[FileOperations] File not found: {file_path}")
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}",
                    "file_path": file_path,
                }

            if not target_path.is_file():
                print(f"[FileOperations] Path is not a file: {file_path}")
                return {
                    "status": "error",
                    "message": f"Path is not a file: {file_path}",
                    "file_path": file_path,
                }

            content = target_path.read_text(encoding="utf-8")
            stat = target_path.stat()
            print(f"[FileOperations] File read successfully: {file_path}")
            return {
                "status": "success",
                "message": f"Read file: {file_path}",
                "content": content,
                "file_path": file_path,
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            }
        except Exception as e:
            error_msg = str(e)
            print(f"[FileOperations] Error reading file: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "file_path": file_path,
            }

    def update_file(self, file_path: str, content: str, append: bool = False) -> Dict[str, Any]:
        try:
            target_path = self._validate_path(file_path)

            if not target_path.exists():
                print(f"[FileOperations] File not found for update: {file_path}")
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}",
                    "file_path": file_path,
                }

            current_content = target_path.read_text(encoding="utf-8")
            new_content = f"{current_content}\n{content}" if append and current_content else (
                current_content + content if append else content
            )

            target_path.write_text(new_content, encoding="utf-8")
            print(f"[FileOperations] File updated successfully: {file_path} (append={append})")
            return {
                "status": "success",
                "message": f"File updated: {file_path}",
                "file_path": file_path,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            error_msg = str(e)
            print(f"[FileOperations] Error updating file: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "file_path": file_path,
            }

    def delete_file(self, file_path: str) -> Dict[str, Any]:
        try:
            target_path = self._validate_path(file_path)

            if not target_path.exists():
                print(f"[FileOperations] File not found for deletion: {file_path}")
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}",
                    "file_path": file_path,
                }

            if not target_path.is_file():
                print(f"[FileOperations] Path is not a file for deletion: {file_path}")
                return {
                    "status": "error",
                    "message": f"Path is not a file: {file_path}",
                    "file_path": file_path,
                }

            target_path.unlink()
            print(f"[FileOperations] File deleted successfully: {file_path}")
            return {
                "status": "success",
                "message": f"File deleted: {file_path}",
                "file_path": file_path,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            error_msg = str(e)
            print(f"[FileOperations] Error deleting file: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "file_path": file_path,
            }

    def rename_file(self, old_path: str, new_path: str) -> Dict[str, Any]:
        try:
            old_target = self._validate_path(old_path)
            new_target = self._validate_path(new_path)

            if not old_target.exists():
                print(f"[FileOperations] Source file not found for rename: {old_path}")
                return {
                    "status": "error",
                    "message": f"File not found: {old_path}",
                    "file_path": old_path,
                }

            if new_target.exists():
                print(f"[FileOperations] Target file already exists: {new_path}")
                return {
                    "status": "error",
                    "message": f"Target file already exists: {new_path}",
                    "file_path": new_path,
                }

            new_target.parent.mkdir(parents=True, exist_ok=True)
            old_target.rename(new_target)
            print(f"[FileOperations] File renamed successfully: {old_path} -> {new_path}")
            return {
                "status": "success",
                "message": f"File renamed: {old_path} to {new_path}",
                "old_path": old_path,
                "new_path": new_path,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            error_msg = str(e)
            print(f"[FileOperations] Error renaming file: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
            }

    def list_files(self, directory: str = "") -> Dict[str, Any]:
        try:
            target_dir = self._validate_path(directory) if directory else self.base_path

            if not target_dir.exists():
                print(f"[FileOperations] Directory not found: {directory}")
                return {
                    "status": "error",
                    "message": f"Directory not found: {directory}",
                }

            files = []
            for item in target_dir.iterdir():
                files.append(
                    {
                        "name": item.name,
                        "type": "folder" if item.is_dir() else "file",
                        "size": item.stat().st_size if item.is_file() else None,
                        "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
                    }
                )

            print(f"[FileOperations] Listed {len(files)} items in: {directory or 'root'}")
            return {
                "status": "success",
                "directory": directory or "root",
                "files": sorted(files, key=lambda x: (x["type"] == "file", x["name"].lower())),
                "count": len(files),
                "message": f"Listed {len(files)} item(s)",
            }
        except Exception as e:
            error_msg = str(e)
            print(f"[FileOperations] Error listing files: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
            }

    def launch_app(self, app_name: str) -> Dict[str, Any]:
        normalized_name = app_name.strip().lower()
        
        # Try exact match first
        target = self.app_aliases.get(normalized_name)
        
        # If no exact match, try fuzzy matching
        if not target:
            for alias, exe in self.app_aliases.items():
                if alias in normalized_name or normalized_name in alias:
                    target = exe
                    normalized_name = alias
                    break
        
        if not target:
            supported = ", ".join(sorted(self.app_aliases.keys()))
            return {
                "status": "error",
                "message": f"Unsupported app '{app_name}'. Supported apps: {supported}",
            }

        try:
            print(f"[FileOperations] Launching app: {normalized_name} ({target})")
            if os.name == "nt":
                os.startfile(target)  # type: ignore[attr-defined]
            else:
             subprocess.Popen([target])

            return {
                "status": "success",
                "message": f"Opened {normalized_name}",
                "app_name": normalized_name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            error_msg = str(e)
            print(f"[FileOperations] Error launching app: {error_msg}")
            return {
                "status": "error",
                "message": f"Failed to open {normalized_name}: {error_msg}",
                "app_name": normalized_name,
            }


file_handler = FileOperationHandler()
