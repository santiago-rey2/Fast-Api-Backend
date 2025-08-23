"""
Rutas para el manejo de Vinos
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.repositories.vinos import VinoRepository
from src.services.vinos import VinoService
from src.schemas.vino import VinoCreate, VinoUpdate, VinoResponse, VinosListResponse

router = APIRouter(prefix="/vinos", tags=["vinos"])

def get_vino_service(db: Session = Depends(get_db)) -> VinoService:
    """Factory para el servicio de vinos"""
    repo = VinoRepository(db)
    return VinoService(repo)

@router.get("/", response_model=VinosListResponse)
def listar_vinos(
    categoria_id: Optional[int] = Query(None, description="ID de la categoría para filtrar"),
    bodega_id: Optional[int] = Query(None, description="ID de la bodega para filtrar"),
    q: Optional[str] = Query(None, description="Búsqueda por nombre"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    ordenar_por: str = Query("nombre", description="Campo para ordenar"),
    service: VinoService = Depends(get_vino_service)
):
    """Lista todos los vinos con filtros opcionales"""
    try:
        vinos, total = service.listar_vinos(categoria_id, bodega_id, q, limit, offset, ordenar_por)
        return VinosListResponse(
            vinos=[VinoResponse.model_validate(vino) for vino in vinos],
            total=total,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener vinos: {str(e)}")

@router.get("/{vino_id}", response_model=VinoResponse)
def obtener_vino(
    vino_id: int,
    service: VinoService = Depends(get_vino_service)
):
    """Obtiene un vino específico por ID"""
    vino = service.obtener_vino(vino_id)
    if not vino:
        raise HTTPException(status_code=404, detail="Vino no encontrado")
    
    return VinoResponse.model_validate(vino)

@router.post("/", response_model=VinoResponse, status_code=201)
def crear_vino(
    vino_data: VinoCreate,
    service: VinoService = Depends(get_vino_service)
):
    """Crea un nuevo vino"""
    try:
        vino = service.crear_vino(vino_data)
        return VinoResponse.model_validate(vino)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear vino: {str(e)}")

@router.put("/{vino_id}", response_model=VinoResponse)
def actualizar_vino(
    vino_id: int,
    vino_data: VinoUpdate,
    service: VinoService = Depends(get_vino_service)
):
    """Actualiza un vino existente"""
    try:
        vino = service.actualizar_vino(vino_id, vino_data)
        if not vino:
            raise HTTPException(status_code=404, detail="Vino no encontrado")
        
        return VinoResponse.model_validate(vino)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar vino: {str(e)}")

@router.delete("/{vino_id}", status_code=204)
def eliminar_vino(
    vino_id: int,
    service: VinoService = Depends(get_vino_service)
):
    """Elimina un vino"""
    try:
        eliminado = service.eliminar_vino(vino_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Vino no encontrado")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar vino: {str(e)}")
