from datetime import datetime

from pydantic import BaseModel


class FileResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    storage_key: str
    content_type: str
    size: int
    created_at: datetime

    class Config:
        from_attributes = True