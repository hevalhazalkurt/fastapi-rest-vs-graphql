from fastapi import APIRouter
from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: str


router = APIRouter(tags=["Server Status"])


@router.get("/status", response_model=StatusResponse)
async def get_server_status():
    """
    Check server status
    """
    return {"status": "ok"}