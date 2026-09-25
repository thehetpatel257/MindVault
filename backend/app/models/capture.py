from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

from pydantic import BaseModel, HttpUrl

class CaptureCreate(BaseModel):
    title: str
    url: HttpUrl | None = None
    content: str
    status: str = "active"


class CaptureResponse(BaseModel):
    id: int
    user_id: int
    title: str
    url: str | None
    content: str
    status: str

    class Config:
        from_attributes = True
class Capture(Base):

    __tablename__ = "captures"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    url: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="active"
    )