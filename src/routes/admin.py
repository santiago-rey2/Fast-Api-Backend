from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.repositories.menu_repository import MenuRepository
from src.schemas.menu_schema import PlatosGroupedResponse
from src.schemas.wines_schema import VinosGroupedResponse

router = APIRouter(prefix="/admin", tags=["Admin"])
@router.get(
    "/saludo"
)
async def saludo():
    return {"mensaje": "Hola, Admin!"}
