import re
from enum import Enum
from typing import Any, Dict


class CommandType(Enum):
    CREATE_FILE = "create_file"
    READ_FILE = "read_file"
    UPDATE_FILE = "update_file"
    DELETE_FILE = "delete_file"
    RENAME_FILE = "rename_file"
    LIST_FILES = "list_files"
    OPEN_APP = "open_app"
    UNKNOWN = "unknown"


class VoiceCommandParser:
    """Parse voice commands and extract intent."""

    def parse(self, transcription: str) -> Dict[str, Any]:
        text = transcription.lower().strip()

        if any(
            phrase in text
            for phrase in [
                "open app",
                "launch",
                "start app",
                "open calculator",
                "open notepad",
                "open paint",
                "open explorer",
                "open powershell",
                "open command prompt",
                "open code",
                "open vs code",
                "run",
                "execute",
                "start",
                "launch app",
                "open the",
                "can you open",
                "please open",
                "open my",
                "open idle",
                "idle",
                "open python",
                "python",
            ]
        ):
            return self._parse_open_app(text)

        if any(word in text for word in ["create", "make", "new file", "make a file", "create file", "create a file", "new", "write file"]):
            return self._parse_create(text)

        if any(word in text for word in ["read", "open file", "show", "get content", "display", "view file", "show file", "can you read", "please read"]):
            return self._parse_read(text)

        if any(word in text for word in ["add", "write", "append", "edit", "update", "modify", "add to", "append to"]):
            return self._parse_update(text)

        if any(word in text for word in ["delete", "remove", "remove file", "erase", "remove the", "delete the", "remove my"]):
            return self._parse_delete(text)

        if any(word in text for word in ["rename", "change name", "rename file", "rename the"]):
            return self._parse_rename(text)

        if any(word in text for word in ["list", "show files", "list files", "show me files", "what files", "list all", "list the", "show directory", "what's in"]):
            return self._parse_list(text)

        return {
            "type": CommandType.UNKNOWN.value,
            "confidence": 0,
            "message": "Could not understand command",
        }

    def _parse_create(self, text: str) -> Dict[str, Any]:
        filename = self._extract_filename(text)
        content = ""
        if " with " in text:
            content = text.split(" with ", 1)[1].strip()
        elif " containing " in text:
            content = text.split(" containing ", 1)[1].strip()

        return {
            "type": CommandType.CREATE_FILE.value,
            "confidence": 0.9,
            "file_path": filename,
            "content": content,
            "message": f"Creating file: {filename}",
        }

    def _parse_read(self, text: str) -> Dict[str, Any]:
        filename = self._extract_filename(text)
        return {
            "type": CommandType.READ_FILE.value,
            "confidence": 0.9,
            "file_path": filename,
            "message": f"Reading file: {filename}",
        }

    def _parse_update(self, text: str) -> Dict[str, Any]:
        filename = self._extract_filename(text)
        content = ""

        if filename in text and " to " in text:
            prefix, _, suffix = text.partition(" to ")
            if filename in suffix:
                content = prefix
        elif " with " in text:
            content = text.split(" with ", 1)[1].strip()
        elif " append " in text:
            content = text.split(" append ", 1)[1].strip()

        for word in ["add", "write", "append", "edit", "update", "to"]:
            content = content.replace(word, "").strip()

        return {
            "type": CommandType.UPDATE_FILE.value,
            "confidence": 0.85,
            "file_path": filename,
            "content": content,
            "append": True,
            "message": f"Updating file: {filename}",
        }

    def _parse_delete(self, text: str) -> Dict[str, Any]:
        filename = self._extract_filename(text)
        return {
            "type": CommandType.DELETE_FILE.value,
            "confidence": 0.9,
            "file_path": filename,
            "message": f"Deleting file: {filename}",
        }

    def _parse_rename(self, text: str) -> Dict[str, Any]:
        files = self._extract_filenames(text)
        if len(files) < 2:
            return {
                "type": CommandType.UNKNOWN.value,
                "confidence": 0,
                "message": "Could not parse rename command",
            }

        return {
            "type": CommandType.RENAME_FILE.value,
            "confidence": 0.9,
            "old_path": files[0],
            "new_path": files[1],
            "message": f"Renaming: {files[0]} to {files[1]}",
        }

    def _parse_list(self, text: str) -> Dict[str, Any]:
        directory = ""
        if " in " in text:
            directory = text.split(" in ", 1)[1].strip()

        return {
            "type": CommandType.LIST_FILES.value,
            "confidence": 0.95,
            "directory": directory,
            "message": f"Listing files in: {directory if directory else 'root'}",
        }

    def _parse_open_app(self, text: str) -> Dict[str, Any]:
        app_name = text
        
        # Common prefixes to remove
        prefixes = [
            "open app", "launch", "start app", "open", "start", 
            "run", "execute", "can you open", "please open", 
            "open my", "open the", "launch app", "please"
        ]
        
        for prefix in prefixes:
            if app_name.startswith(prefix):
                app_name = app_name[len(prefix):].strip()
                # Keep removing if there are multiple prefixes
                remaining_text = app_name
                for next_prefix in prefixes:
                    if remaining_text.startswith(next_prefix):
                        app_name = remaining_text[len(next_prefix):].strip()
                        break
                break

        # Handle common app name variations
        app_name = app_name.strip(" .,!?").lower()
        
        # Normalize common names
        name_map = {
            "notepad": "notepad",
            "calc": "calculator",
            "paint": "paint",
            "explorer": "explorer",
            "cmd": "command prompt",
            "powershell": "powershell",
            "vscode": "vscode",
            "code": "vscode",
            "vs code": "vscode",
            "visual studio code": "vscode",
        }
        
        # Try exact match first
        if app_name in name_map:
            app_name = name_map[app_name]
        
        # Then try partial matches
        for key, value in name_map.items():
            if key in app_name:
                app_name = value
                break

        return {
            "type": CommandType.OPEN_APP.value,
            "confidence": 0.85,
            "app_name": app_name or "unknown",
            "message": f"Opening {app_name or 'application'}",
        }

    def _extract_filename(self, text: str) -> str:
        normalized = text.lower()
        normalized = normalized.replace(" dot ", ".")
        normalized = normalized.replace(" txt", ".txt")
        normalized = normalized.replace(" text file", ".txt")
        normalized = normalized.replace(" python file", ".py")
        normalized = normalized.replace(" py file", ".py")
        normalized = normalized.replace(" json file", ".json")
        normalized = normalized.replace(" csv file", ".csv")
        normalized = normalized.replace(" excel file", ".excel")

        # First try to find quoted filenames
        quoted = re.findall(r'"([^"]+)"', text)
        if quoted:
            return quoted[0].strip()

        # Try to find filenames after common phrases
        patterns = [
            r'called\s+([a-z0-9._\\/-]+)',
            r'named\s+([a-z0-9._\\/-]+)',
            r'file\s+(?:called\s+)?([a-z0-9._\\/-]+)',
            r'file\s+(?:named\s+)?([a-z0-9._\\/-]+)',
            r'file\s+(?:with\s+)?(?:name\s+)?(?:of\s+)?([a-z0-9._\\/-]+)',
            r'([a-z0-9._\\/-]+\.[a-z0-9]+)',
            r'as\s+([a-z0-9._\\/-]+)',
            r'to\s+([a-z0-9._\\/-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, normalized)
            if match:
                filename = match.group(1).strip(" .")
                if filename and not any(word in filename for word in ["create", "make", "new", "file", "called", "named", "with", "to", "as"]):
                    return filename

        return "unnamed.txt"

    def _extract_filenames(self, text: str) -> list[str]:
        filenames = re.findall(r"[a-z0-9._\\/-]+\.[a-z0-9]+", text.lower())
        return filenames if filenames else []


command_parser = VoiceCommandParser()
