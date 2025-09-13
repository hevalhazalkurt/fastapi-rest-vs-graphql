from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db


class StatusResponse(BaseModel):
    status: str


class HealthResponse(BaseModel):
    status: str
    db_status: str


router = APIRouter()


@router.get("/status", response_model=StatusResponse)
async def get_server_status():
    """
    Check server status
    """
    return {"status": "ok"}


@router.get("/health", response_model=HealthResponse)
async def get_server_health(db: AsyncSession = Depends(get_db)):
    """
    Check server status
    """
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar_one()
        db_status = "ok"
    except Exception as e:
        print(f"Database connection failed: {e}")
        db_status = "error"

    return {"status": "ok", "db_status": db_status}
