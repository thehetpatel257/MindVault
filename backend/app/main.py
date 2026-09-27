from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine, Base
from app.models import User, Capture, File
from app.api.users import router as users_router
from app.api.captures import router as captures_router
from app.api.files import router as files_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.security_headers import SecurityHeadersMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MindVault API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.add_middleware(SecurityHeadersMiddleware)
app.include_router(users_router)
app.include_router(captures_router)
app.include_router(files_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MindVault API"
    }

@app.get("/health/db")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "not connected",
            "detail": str(e)
        }