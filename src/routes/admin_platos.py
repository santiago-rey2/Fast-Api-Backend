"""
Rutas de administración para la gestión de platos
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.dependencies import get_current_admin_user
from src.entities.user import User
from src.repositories.platos import PlatoRepository
from src.services.platos import PlatoService
from src.schemas.plato import PlatoCreate, PlatoUpdate, PlatoResponse, PlatosListResponse

router = APIRouter(
    prefix="/admin/platos",
    tags=["👨‍💼 Administración - Gestión de Platos"],
    dependencies=[Depends(get_current_admin_user)],
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Permisos de administrador requeridos"},
        404: {"description": "Plato no encontrado"}
    }
)

def get_plato_service(db: Session = Depends(get_db)) -> PlatoService:
    """Factory para el servicio de platos"""
    repo = PlatoRepository(db)
    return PlatoService(repo)

@router.get(
    "/",
    response_model=PlatosListResponse,
    summary="📋 Listar todos los platos (incluidos inactivos)",
    description="Obtiene una lista completa de platos para administración, incluyendo platos inactivos y eliminados.",
    response_description="Lista completa de platos con información de paginación"
)
def listar_platos_admin(
    categoria_id: Optional[int] = Query(None, description="ID de la categoría para filtrar"),
    q: Optional[str] = Query(None, description="Búsqueda por nombre"),
    incluir_inactivos: bool = Query(False, description="Incluir platos inactivos"),
    incluir_eliminados: bool = Query(False, description="Incluir platos eliminados"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    ordenar_por: str = Query("nombre", description="Campo para ordenar"),
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Lista todos los platos para administración con filtros avanzados"""
    try:
        platos, total = service.listar_platos_admin(
            categoria_id, q, incluir_inactivos, incluir_eliminados, limit, offset, ordenar_por
        )
        return PlatosListResponse(
            platos=[PlatoResponse.model_validate(plato) for plato in platos],
            total=total,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener platos: {str(e)}")

@router.post(
    "/",
    response_model=PlatoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="➕ Crear nuevo plato",
    description="Crea un nuevo plato en el sistema con toda la información necesaria.",
    response_description="Plato creado con éxito"
)
def crear_plato(
    plato_data: PlatoCreate,
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Crea un nuevo plato"""
    try:
        plato = service.crear_plato(plato_data)
        return PlatoResponse.model_validate(plato)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear plato: {str(e)}")

@router.get(
    "/{plato_id}",
    response_model=PlatoResponse,
    summary="🔍 Obtener plato específico (admin)",
    description="Obtiene la información completa de un plato específico, incluyendo datos administrativos.",
    response_description="Información detallada del plato"
)
def obtener_plato_admin(
    plato_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Obtiene un plato específico para administración"""
    plato = service.obtener_plato_admin(plato_id)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    return PlatoResponse.model_validate(plato)

@router.put(
    "/{plato_id}",
    response_model=PlatoResponse,
    summary="✏️ Actualizar plato",
    description="Actualiza la información de un plato existente.",
    response_description="Plato actualizado con éxito"
)
def actualizar_plato(
    plato_id: int,
    plato_data: PlatoUpdate,
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Actualiza un plato existente"""
    try:
        plato = service.actualizar_plato(plato_id, plato_data)
        if not plato:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        return PlatoResponse.model_validate(plato)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar plato: {str(e)}")

@router.delete(
    "/{plato_id}",
    summary="🗑️ Eliminar plato (soft delete)",
    description="Marca un plato como eliminado (soft delete) manteniéndolo en la base de datos.",
    response_description="Confirmación de eliminación"
)
def eliminar_plato(
    plato_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Elimina un plato (soft delete)"""
    try:
        success = service.eliminar_plato(plato_id)
        if not success:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        return {"message": "Plato eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar plato: {str(e)}")

@router.post(
    "/{plato_id}/restore",
    response_model=PlatoResponse,
    summary="♻️ Restaurar plato eliminado",
    description="Restaura un plato que fue marcado como eliminado.",
    response_description="Plato restaurado con éxito"
)
def restaurar_plato(
    plato_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Restaura un plato eliminado"""
    try:
        plato = service.restaurar_plato(plato_id)
        if not plato:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        return PlatoResponse.model_validate(plato)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al restaurar plato: {str(e)}")

@router.patch(
    "/{plato_id}/toggle-active",
    response_model=PlatoResponse,
    summary="🔄 Cambiar estado activo/inactivo",
    description="Alterna el estado activo/inactivo de un plato.",
    response_description="Plato con estado actualizado"
)
def toggle_plato_activo(
    plato_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: PlatoService = Depends(get_plato_service)
):
    """Cambia el estado activo/inactivo de un plato"""
    try:
        plato = service.toggle_activo(plato_id)
        if not plato:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        return PlatoResponse.model_validate(plato)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cambiar estado: {str(e)}")
