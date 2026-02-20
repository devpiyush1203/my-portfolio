from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from pathlib import Path
import logging
import sys

sys.path.append(str(Path(__file__).parent.parent))

from models import ResumeMetadata

logger = logging.getLogger(__name__)
router = APIRouter()

# Database will be injected by server.py
db = None

def set_db(database):
    global db
    db = database

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a new resume file
    """
    try:
        # Validate file type
        allowed_types = ['application/pdf', 'application/msword', 
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and Word documents are allowed"
            )
        
        # Generate safe filename
        file_extension = os.path.splitext(file.filename)[1]
        safe_filename = f"resume_piyush_malviya{file_extension}"
        file_path = UPLOADS_DIR / safe_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Mark all existing resumes as inactive
        await db.resumes.update_many({}, {"$set": {"is_active": False}})
        
        # Create metadata
        resume_metadata = ResumeMetadata(
            filename=safe_filename,
            original_name=file.filename,
            mime_type=file.content_type,
            size=os.path.getsize(file_path),
            file_path=str(file_path),
            is_active=True
        )
        
        # Save metadata to database
        await db.resumes.insert_one(resume_metadata.dict())
        
        logger.info(f"Resume uploaded successfully: {safe_filename}")
        return {
            "success": True,
            "message": "Resume uploaded successfully",
            "filename": safe_filename
        }
        
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/resume/download")
async def download_resume():
    """
    Download the active resume file
    """
    try:
        # Get active resume from database
        resume = await db.resumes.find_one({"is_active": True})
        
        if not resume:
            raise HTTPException(
                status_code=404,
                detail="No resume available for download"
            )
        
        file_path = Path(resume['file_path'])
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Resume file not found on server"
            )
        
        logger.info(f"Resume downloaded: {resume['filename']}")
        return FileResponse(
            path=str(file_path),
            filename=resume['original_name'],
            media_type=resume['mime_type']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/resume/current")
async def get_current_resume():
    """
    Get metadata of the current active resume
    """
    try:
        resume = await db.resumes.find_one({"is_active": True})
        
        if not resume:
            return {"has_resume": False}
        
        return {
            "has_resume": True,
            "filename": resume['original_name'],
            "uploaded_at": resume['uploaded_at'],
            "size": resume['size']
        }
        
    except Exception as e:
        logger.error(f"Error getting resume metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
