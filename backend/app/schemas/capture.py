from pydantic import BaseModel, HttpUrl


class CaptureCreate(BaseModel):
    title: str
    url: HttpUrl
    content: str
    status: str = "saved"

class CaptureUpdate(BaseModel):
    title: str | None = None
    url: HttpUrl | None = None
    content: str | None = None
    status: str | None = None
    
class CaptureResponse(BaseModel):
    id: int
    user_id: int
    title: str
    url: str
    content: str
    status: str

    class Config:
        from_attributes = True