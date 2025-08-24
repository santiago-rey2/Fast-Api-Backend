"""
Rutas de administración para la gestión de vinos
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.dependencies import get_current_admin_user
from src.entities.user import User
from src.repositories.vinos import VinoRepository
from src.services.vinos import VinoService
from src.schemas.vino import VinoCreate, VinoUpdate, VinoResponse, VinosListResponse

router = APIRouter(
    prefix="/admin/vinos",
    tags=["👨‍💼 Administración - Gestión de Vinos"],
    dependencies=[Depends(get_current_admin_user)],
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Permisos de administrador requeridos"},
        404: {"description": "Vino no encontrado"}
    }
)

def get_vino_service(db: Session = Depends(get_db)) -> VinoService:
    """Factory para el servicio de vinos"""
    repo = VinoRepository(db)
    return VinoService(repo)

@router.get(
    "/",
    response_model=VinosListResponse,
    summary="📋 Listar todos los vinos (incluidos inactivos)",
    description="Obtiene una lista completa de vinos para administración, incluyendo vinos inactivos y eliminados.",
    response_description="Lista completa de vinos con información de paginación"
)
def listar_vinos_admin(
    categoria_id: Optional[int] = Query(None, description="ID de la categoría para filtrar"),
    bodega_id: Optional[int] = Query(None, description="ID de la bodega para filtrar"),
    q: Optional[str] = Query(None, description="Búsqueda por nombre"),
    incluir_inactivos: bool = Query(False, description="Incluir vinos inactivos"),
    incluir_eliminados: bool = Query(False, description="Incluir vinos eliminados"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    ordenar_por: str = Query("nombre", description="Campo para ordenar"),
    current_admin: User = Depends(get_current_admin_user),
    service: VinoService = Depends(get_vino_service)
):
    """Lista todos los vinos para administración con filtros avanzados"""
    try:
        vinos, total = service.listar_vinos_admin(
            categoria_id, bodega_id, q, incluir_inactivos, incluir_eliminados, limit, offset, ordenar_por
        )
        return VinosListResponse(
            vinos=[VinoResponse.model_validate(vino) for vino in vinos],
            total=total,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener vinos: {str(e)}")

@router.post(
    "/",
    response_model=VinoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="➕ Crear nuevo vino",
    description="Crea un nuevo vino en el sistema con toda la información necesaria.",
    response_description="Vino creado con éxito"
)
def crear_vino(
    vino_data: VinoCreate,
    current_admin: User = Depends(get_current_admin_user),
    service: VinoService = Depends(get_vino_service)
):
    """Crea un nuevo vino"""
    try:
        vino = service.crear_vino(vino_data)
        return VinoResponse.model_validate(vino)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear vino: {str(e)}")

@router.get(
    "/{vino_id}",
    response_model=VinoResponse,
    summary="🔍 Obtener vino específico (admin)",
    description="Obtiene la información completa de un vino específico, incluyendo datos administrativos.",
    response_description="Información detallada del vino"
)
def obtener_vino_admin(
    vino_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: VinoService = Depends(get_vino_service)
):
    """Obtiene un vino específico para administración"""
    vino = service.obtener_vino_admin(vino_id)
    if not vino:
        raise HTTPException(status_code=404, detail="Vino no encontrado")
    return VinoResponse.model_validate(vino)

@router.put(
    "/{vino_id}",
    response_model=VinoResponse,
    summary="✏️ Actualizar vino",
    description="Actualiza la información de un vino existente.",
    response_description="Vino actualizado con éxito"
)
def actualizar_vino(
    vino_id: int,
    vino_data: VinoUpdate,
    current_admin: User = Depends(get_current_admin_user),
    service: VinoService = Depends(get_vino_service)
):
    """Actualiza un vino existente"""
    try:
        vino = service.actualizar_vino(vino_id, vino_data)
        if not vino:
            raise HTTPException(status_code=404, detail="Vino no encontrado")
        return VinoResponse.model_validate(vino)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar vino: {str(e)}")

@router.delete(
    "/{vino_id}",
    summary="🗑️ Eliminar vino (soft delete)",
    description="Marca un vino como eliminado (soft delete) manteniéndolo en la base de datos.",
    response_description="Confirmación de eliminación"
)
def eliminar_vino(
    vino_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: VinoService = Depends(get_vino_service)
):
    """Elimina un vino (soft delete)"""
    try:
        success = service.eliminar_vino(vino_id)
        if not success:
            raise HTTPException(status_code=404, detail="Vino no encontrado")
        return {"message": "Vino eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar vino: {str(e)}")

@router.post(
    "/{vino_id}/restore",
    response_model=VinoResponse,
    summary="♻️ Restaurar vino eliminado",
    description="Restaura un vino que fue marcado como eliminado.",
    response_description="Vino restaurado con éxito"
)
def restaurar_vino(
    vino_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: VinoService = Depends(get_vino_service)
):
    """Restaura un vino eliminado"""
    try:
        vino = service.restaurar_vino(vino_id)
        if not vino:
            raise HTTPException(status_code=404, detail="Vino no encontrado")
        return VinoResponse.model_validate(vino)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al restaurar vino: {str(e)}")

@router.patch(
    "/{vino_id}/toggle-active",
    response_model=VinoResponse,
    summary="🔄 Cambiar estado activo/inactivo",
    description="Alterna el estado activo/inactivo de un vino.",
    response_description="Vino con estado actualizado"
)
def toggle_vino_activo(
    vino_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: VinoService = Depends(get_vino_service)
):
    """Cambia el estado activo/inactivo de un vino"""
    try:
        vino = service.toggle_activo(vino_id)
        if not vino:
            raise HTTPException(status_code=404, detail="Vino no encontrado")
        return VinoResponse.model_validate(vino)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cambiar estado: {str(e)}")
