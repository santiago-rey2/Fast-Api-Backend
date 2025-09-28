from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.repositories.menu_repository import MenuRepository

router = APIRouter(tags=["Menu"])

@router.get("/platos")
async def get_platos(db: Session = Depends(get_db)):
    """
    Obtiene todos los platos agrupados por categoría
    """
    try:
        menu_repo = MenuRepository(db)
        platos_agrupados = menu_repo.get_platos_agrupados_por_categoria()
        return {"platos": platos_agrupados}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener platos: {str(e)}")

@router.get("/vinos")
async def get_vinos():
    """Obtener lista de vinos"""
    return [{"message": "Lista de vinos esta viva" }]
