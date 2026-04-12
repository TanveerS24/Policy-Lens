from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from typing import Optional
from bson import ObjectId

from app.database.client import get_db


class GridFSHelper:
    """Helper for MongoDB GridFS operations"""
    
    @staticmethod
    async def get_gridfs():
        """Get GridFS bucket instance"""
        db = get_db()
        return AsyncIOMotorGridFSBucket(db, bucket_name="profile_photos")
    
    @staticmethod
    async def upload_file(
        filename: str,
        file_data: bytes,
        content_type: str,
        metadata: Optional[dict] = None
    ) -> str:
        """
        Upload file to GridFS
        
        Args:
            filename: Original filename
            file_data: File bytes
            content_type: MIME type
            metadata: Optional metadata dict
        
        Returns:
            str: File ID
        """
        gridfs = await GridFSHelper.get_gridfs()
        
        file_id = await gridfs.upload_from_stream(
            filename=filename,
            source=file_data,
            metadata=metadata or {},
            content_type=content_type
        )
        
        return str(file_id)
    
    @staticmethod
    async def get_file(file_id: str):
        """
        Get file from GridFS
        
        Args:
            file_id: File ID
        
        Returns:
            GridOut file object
        """
        gridfs = await GridFSHelper.get_gridfs()
        
        try:
            return await gridfs.open_download_stream(ObjectId(file_id))
        except Exception:
            return None
    
    @staticmethod
    async def delete_file(file_id: str) -> bool:
        """
        Delete file from GridFS
        
        Args:
            file_id: File ID
        
        Returns:
            bool: True if deleted
        """
        gridfs = await GridFSHelper.get_gridfs()
        
        try:
            await gridfs.delete(ObjectId(file_id))
            return True
        except Exception:
            return False


gridfs_helper = GridFSHelper()
