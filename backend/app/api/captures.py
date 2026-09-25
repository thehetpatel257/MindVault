from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.capture import Capture
from app.schemas.capture import (
    CaptureCreate,
    CaptureUpdate,
    CaptureResponse
)
from app.core.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/captures",
    tags=["Captures"]
)


@router.post(
    "",
    response_model=CaptureResponse
)
def create_capture(
    capture_data: CaptureCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    capture = Capture(
        user_id=current_user.id,
        title=capture_data.title,
        url=str(capture_data.url) if capture_data.url else None,
        content=capture_data.content,
        status=capture_data.status
    )

    db.add(capture)
    db.commit()
    db.refresh(capture)

    return capture

@router.get(
    "",
    response_model=list[CaptureResponse]
)
def get_my_captures(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    captures = (
        db.query(Capture)
        .filter(Capture.user_id == current_user.id)
        .all()
    )

    return captures

@router.get(
    "/{capture_id}",
    response_model=CaptureResponse
)
def get_capture(
    capture_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    capture = (
        db.query(Capture)
        .filter(
            Capture.id == capture_id,
            Capture.user_id == current_user.id
        )
        .first()
    )

    if not capture:
        raise HTTPException(
            status_code=404,
            detail="Capture not found"
        )

    return capture

@router.put(
    "/{capture_id}",
    response_model=CaptureResponse
)
def update_capture(
    capture_id: int,
    capture_data: CaptureUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    capture = (
        db.query(Capture)
        .filter(
            Capture.id == capture_id,
            Capture.user_id == current_user.id
        )
        .first()
    )

    if not capture:
        raise HTTPException(
            status_code=404,
            detail="Capture not found"
        )

    if capture_data.title is not None:
        capture.title = capture_data.title

    if capture_data.url is not None:
        capture.url = str(capture_data.url)

    if capture_data.content is not None:
        capture.content = capture_data.content

    if capture_data.status is not None:
        capture.status = capture_data.status

    db.commit()
    db.refresh(capture)

    return capture

@router.delete("/{capture_id}")
def delete_capture(
    capture_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    capture = (
        db.query(Capture)
        .filter(
            Capture.id == capture_id,
            Capture.user_id == current_user.id
        )
        .first()
    )

    if not capture:
        raise HTTPException(
            status_code=404,
            detail="Capture not found"
        )

    db.delete(capture)
    db.commit()

    return {
        "message": "Capture deleted successfully"
    }