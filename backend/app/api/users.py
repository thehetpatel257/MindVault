from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.core.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Response

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/login")
def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    # Store JWT in cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,       # Change to True when using HTTPS
        samesite="lax",
        max_age=30 * 60
    )

    return {
        "message": "Login successful",
        "token_type": "bearer"
    }

@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie(
        key="access_token"
    )

    return {
        "message": "Logout successful"
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user_data.password
    )

    user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user