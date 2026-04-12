from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.utils.gridfs_helper import gridfs_helper

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/{file_id}")
async def get_file(file_id: str):
    """Get file by ID (public endpoint for profile photos, etc.)"""
    file_stream = await gridfs_helper.get_file(file_id)
    
    if not file_stream:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Read file data
    file_data = await file_stream.read()
    
    # Get content type from metadata or default
    content_type = getattr(file_stream, "content_type", "application/octet-stream")
    
    return Response(
        content=file_data,
        media_type=content_type,
        headers={"Content-Disposition": f"inline; filename={file_stream.filename}"}
    )
