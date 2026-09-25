import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File as FastAPIFile,
    HTTPException,
    UploadFile
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.file import File
from app.models.user import User
from app.schemas.file import FileResponse as FileResponseSchema


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# Maximum file size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024


# Allowed file types
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "text/plain",
    "image/jpeg",
    "image/png",
    "image/webp"
}


# ============================================================
# UPLOAD FILE
# ============================================================

@router.post(
    "/upload",
    response_model=FileResponseSchema
)
async def upload_file(
    uploaded_file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Validate filename
    if not uploaded_file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    # Validate file type
    if uploaded_file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )

    # Get original filename safely
    original_filename = os.path.basename(
        uploaded_file.filename
    )

    # Generate unique storage name
    storage_key = (
        f"{uuid.uuid4()}_{original_filename}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        storage_key
    )

    total_size = 0

    try:

        # Save file in chunks
        with open(file_path, "wb") as buffer:

            while True:

                chunk = await uploaded_file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                total_size += len(chunk)

                # Check file size
                if total_size > MAX_FILE_SIZE:

                    if os.path.exists(file_path):
                        os.remove(file_path)

                    raise HTTPException(
                        status_code=413,
                        detail="File size exceeds 10 MB limit"
                    )

                buffer.write(chunk)

        # Save metadata in PostgreSQL
        file_record = File(
            user_id=current_user.id,
            filename=original_filename,
            storage_key=storage_key,
            content_type=uploaded_file.content_type,
            size=total_size
        )

        db.add(file_record)
        db.commit()
        db.refresh(file_record)

        return file_record

    except HTTPException:
        raise

    except Exception:

        # Remove file if database operation fails
        if os.path.exists(file_path):
            os.remove(file_path)

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="File upload failed"
        )


# ============================================================
# DOWNLOAD FILE
# ============================================================

@router.get("/{file_id}")
def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find file belonging to logged-in user
    file_record = (
        db.query(File)
        .filter(
            File.id == file_id,
            File.user_id == current_user.id
        )
        .first()
    )

    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    # Build physical file path
    file_path = os.path.join(
        UPLOAD_DIR,
        file_record.storage_key
    )

    # Check if physical file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Physical file not found"
        )

    # Return the file
    return FileResponse(
        path=file_path,
        media_type=file_record.content_type,
        filename=file_record.filename
    )

# ============================================================
# DELETE FILE
# ============================================================

@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find file belonging to logged-in user
    file_record = (
        db.query(File)
        .filter(
            File.id == file_id,
            File.user_id == current_user.id
        )
        .first()
    )

    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    # Build physical file path
    file_path = os.path.join(
        UPLOAD_DIR,
        file_record.storage_key
    )

    # Delete physical file
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete database metadata
    db.delete(file_record)
    db.commit()

    return {
        "message": "File deleted successfully"
    }