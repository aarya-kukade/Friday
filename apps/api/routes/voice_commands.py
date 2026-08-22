from fastapi import APIRouter
from pydantic import BaseModel
from apps.api.core.command_parser import command_parser, CommandType

from apps.api.core.file_operations import file_handler

router = APIRouter(prefix="/api/voice", tags=["voice"])

class VoiceCommandRequest(BaseModel):
    transcription: str

class VoiceCommandResponse(BaseModel):
    status: str
    message: str
    command_type: str
    result: dict | None = None

@router.post("/execute")
async def execute_voice_command(request: VoiceCommandRequest) -> VoiceCommandResponse:
    """
    Parse voice command and execute file operation
    
    Example input: "Create a file called notes.txt"
    """
    
    # Parse the voice command
    parsed = command_parser.parse(request.transcription)
    
    command_type = parsed.get("type", CommandType.UNKNOWN.value)
    message = parsed.get("message", "Processing command...")
    
    print(f"[VoiceAPI] Parsed command: type={command_type}, transcription='{request.transcription[:60]}...'")
    
    # Execute based on command type
    result = None
    
    try:
        if command_type == CommandType.CREATE_FILE.value:
            print(f"[VoiceAPI] Executing: CREATE_FILE {parsed.get('file_path')}")
            result = file_handler.create_file(
                parsed.get("file_path"),
                parsed.get("content", "")
            )
        
        elif command_type == CommandType.READ_FILE.value:
            print(f"[VoiceAPI] Executing: READ_FILE {parsed.get('file_path')}")
            result = file_handler.read_file(parsed.get("file_path"))
        
        elif command_type == CommandType.UPDATE_FILE.value:
            print(f"[VoiceAPI] Executing: UPDATE_FILE {parsed.get('file_path')}")
            result = file_handler.update_file(
                parsed.get("file_path"),
                parsed.get("content"),
                parsed.get("append", True)
            )
        
        elif command_type == CommandType.DELETE_FILE.value:
            print(f"[VoiceAPI] Executing: DELETE_FILE {parsed.get('file_path')}")
            result = file_handler.delete_file(parsed.get("file_path"))
        
        elif command_type == CommandType.RENAME_FILE.value:
            print(f"[VoiceAPI] Executing: RENAME_FILE {parsed.get('old_path')} -> {parsed.get('new_path')}")
            result = file_handler.rename_file(
                parsed.get("old_path"),
                parsed.get("new_path")
            )
        
        elif command_type == CommandType.LIST_FILES.value:
            print(f"[VoiceAPI] Executing: LIST_FILES {parsed.get('directory')}")
            result = file_handler.list_files(parsed.get("directory", ""))

        elif command_type == CommandType.OPEN_APP.value:
            print(f"[VoiceAPI] Executing: OPEN_APP {parsed.get('app_name')}")
            result = file_handler.launch_app(parsed.get("app_name", ""))
        
        else:
            print(f"[VoiceAPI] Unknown command type: {command_type}")
            return VoiceCommandResponse(
                status="error",
                message="I didn't understand that command",
                command_type=command_type,
                result=None
            )
        
        # Return result
        status = "success" if result.get("status") == "success" else "error"
        response_message = result.get("message", message)

        if command_type == CommandType.READ_FILE.value and result.get("status") == "success":
            file_content = str(result.get("content", "")).strip()
            response_message = (
                f"Read {parsed.get('file_path')}. "
                f"{file_content if file_content else 'The file is empty.'}"
            )

        if command_type == CommandType.LIST_FILES.value and result.get("status") == "success":
            names = [item["name"] for item in result.get("files", [])]
            response_message = (
                "No files found."
                if not names
                else "Files: " + ", ".join(names)
            )
        
        print(f"[VoiceAPI] Response: status={status}, message='{response_message[:60]}...'")
        
        return VoiceCommandResponse(
            status=status,
            message=response_message,
            command_type=command_type,
            result=result
        )
    
    except Exception as e:
        error_msg = str(e)
        print(f"[VoiceAPI] Error executing command: {error_msg}")
        return VoiceCommandResponse(
            status="error",
            message=f"Error executing command: {error_msg}",
            command_type=command_type,
            result=None
        )
