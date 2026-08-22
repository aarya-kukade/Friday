"""
File Operations API Routes
Handles file CRUD operations and listing
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from apps.api.core.file_operations import file_handler

router = APIRouter(prefix="/api/files", tags=["files"])

# Request/Response Models
class CreateFileRequest(BaseModel):
    file_path: str
    content: str = ""

class UpdateFileRequest(BaseModel):
    file_path: str
    content: str
    append: bool = False

class RenameFileRequest(BaseModel):
    old_path: str
    new_path: str

class DeleteFileRequest(BaseModel):
    file_path: str

# Routes

@router.post("/create")
async def create_file(request: CreateFileRequest):
    """Create a new file"""
    result = file_handler.create_file(request.file_path, request.content)
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.get("/read")
async def read_file(file_path: str = Query(...)):
    """Read file content"""
    result = file_handler.read_file(file_path)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result

@router.post("/update")
async def update_file(request: UpdateFileRequest):
    """Update file content"""
    result = file_handler.update_file(
        request.file_path,
        request.content,
        request.append
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.post("/delete")
async def delete_file(request: DeleteFileRequest):
    """Delete a file"""
    result = file_handler.delete_file(request.file_path)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result

@router.post("/rename")
async def rename_file(request: RenameFileRequest):
    """Rename a file"""
    result = file_handler.rename_file(request.old_path, request.new_path)
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.get("/list")
async def list_files(directory: str = Query("")):
    """List files in directory"""
    result = file_handler.list_files(directory)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result