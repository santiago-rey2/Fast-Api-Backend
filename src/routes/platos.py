"""
Rutas para el manejo de Platos
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.dependencies import get_current_admin_user
from src.entities.user import User
from src.repositories.platos import PlatoRepository
from src.services.platos import PlatoService
from src.schemas.plato import PlatoCreate, PlatoUpdate, PlatoResponse, PlatosListResponse

router = APIRouter(prefix="/platos", tags=["platos"])

def get_plato_service(db: Session = Depends(get_db)) -> PlatoService:
    """Factory para el servicio de platos"""
    repo = PlatoRepository(db)
    return PlatoService(repo)

@router.get("/", response_model=PlatosListResponse)
def listar_platos(
    categoria_id: Optional[int] = Query(None, description="ID de la categoría para filtrar"),
    q: Optional[str] = Query(None, description="Búsqueda por nombre"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    ordenar_por: str = Query("nombre", description="Campo para ordenar"),
    service: PlatoService = Depends(get_plato_service)
):
    """Lista todos los platos con filtros opcionales"""
    try:
        platos, total = service.listar_platos(categoria_id, q, limit, offset, ordenar_por)
        return PlatosListResponse(
            platos=[PlatoResponse.model_validate(plato) for plato in platos],
            total=total,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener platos: {str(e)}")

@router.get("/{plato_id}", response_model=PlatoResponse)
def obtener_plato(
    plato_id: int,
    service: PlatoService = Depends(get_plato_service)
):
    """Obtiene un plato específico por ID"""
    plato = service.obtener_plato(plato_id)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    
    return PlatoResponse.model_validate(plato)

@router.post("/", response_model=PlatoResponse, status_code=201)
def crear_plato(
    plato_data: PlatoCreate,
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Crea un nuevo plato (requiere autenticación de administrador)"""
    try:
        plato = service.crear_plato(plato_data)
        return PlatoResponse.model_validate(plato)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear plato: {str(e)}")

@router.put("/{plato_id}", response_model=PlatoResponse)
def actualizar_plato(
    plato_id: int,
    plato_data: PlatoUpdate,
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Actualiza un plato existente (requiere autenticación de administrador)"""
    try:
        plato = service.actualizar_plato(plato_id, plato_data)
        if not plato:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        
        return PlatoResponse.model_validate(plato)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar plato: {str(e)}")

@router.delete("/{plato_id}", status_code=204)
def eliminar_plato(
    plato_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Elimina un plato (requiere autenticación de administrador)"""
    try:
        eliminado = service.eliminar_plato(plato_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar plato: {str(e)}")
