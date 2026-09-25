from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.database import engine, Base
from app.models import User, Capture, File
from app.api.users import router as users_router
from app.api.captures import router as captures_router
from app.api.files import router as files_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MindVault API",
    version="1.0.0"
)


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