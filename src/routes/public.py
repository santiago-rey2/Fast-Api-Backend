"""
Rutas públicas para consulta de datos sin autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from src.database import get_db
from src.entities.categoria_plato import CategoriaPlato
from src.entities.alergeno import Alergeno
from src.entities.categoria_vino import CategoriaVino
from src.entities.bodega import Bodega
from src.entities.denominacion_origen import DenominacionOrigen
from src.entities.enologo import Enologo
from src.entities.uva import Uva
from src.repositories.platos import PlatoRepository
from src.repositories.vinos import VinoRepository
from src.services.platos import PlatoService
from src.services.vinos import VinoService
from src.schemas.admin import (
    CategoriaOut, AlerganoOut, CategoriaVinoOut, BodegaOut,
    DenominacionOrigenOut, EnologoOut, UvaOut
)
from src.schemas.plato import PlatoResponse, PlatosListResponse
from src.schemas.vino import VinoResponse, VinosListResponse

router = APIRouter(
    prefix="/public",
    tags=["🌍 Consulta Pública - Datos Completos"],
    responses={
        404: {"description": "Recurso no encontrado"},
        500: {"description": "Error interno del servidor"}
    }
)

# ==================== SERVICIOS ====================

def get_plato_service(db: Session = Depends(get_db)) -> PlatoService:
    """Factory para el servicio de platos"""
    repo = PlatoRepository(db)
    return PlatoService(repo)

def get_vino_service(db: Session = Depends(get_db)) -> VinoService:
    """Factory para el servicio de vinos"""
    repo = VinoRepository(db)
    return VinoService(repo)

# ==================== PLATOS ====================

@router.get(
    "/platos",
    response_model=PlatosListResponse,
    summary="🍽️ Listar platos públicos",
    description="Obtiene una lista paginada de platos activos con filtros opcionales por categoría y búsqueda por nombre.",
    response_description="Lista de platos activos con información de paginación"
)
def listar_platos_publicos(
    categoria_id: Optional[int] = Query(None, description="ID de la categoría para filtrar"),
    q: Optional[str] = Query(None, description="Búsqueda por nombre"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    ordenar_por: str = Query("nombre", description="Campo para ordenar"),
    service: PlatoService = Depends(get_plato_service)
):
    """Lista todos los platos activos con filtros opcionales"""
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

@router.get(
    "/platos/{plato_id}",
    response_model=PlatoResponse,
    summary="🍽️ Obtener plato específico",
    description="Obtiene la información completa de un plato específico incluyendo categoría, alérgenos y precios.",
    response_description="Información detallada del plato"
)
def obtener_plato_publico(
    plato_id: int,
    service: PlatoService = Depends(get_plato_service)
):
    """Obtiene un plato específico por ID"""
    plato = service.obtener_plato(plato_id)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    
    return PlatoResponse.model_validate(plato)

# ==================== VINOS ====================

@router.get(
    "/vinos",
    response_model=VinosListResponse,
    summary="🍷 Listar vinos públicos",
    description="Obtiene una lista paginada de vinos activos con filtros opcionales por categoría, bodega y búsqueda por nombre.",
    response_description="Lista de vinos activos con información de paginación"
)
def listar_vinos_publicos(
    categoria_id: Optional[int] = Query(None, description="ID de la categoría para filtrar"),
    bodega_id: Optional[int] = Query(None, description="ID de la bodega para filtrar"),
    q: Optional[str] = Query(None, description="Búsqueda por nombre"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    ordenar_por: str = Query("nombre", description="Campo para ordenar"),
    service: VinoService = Depends(get_vino_service)
):
    """Lista todos los vinos activos con filtros opcionales"""
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

@router.get(
    "/vinos/{vino_id}",
    response_model=VinoResponse,
    summary="🍷 Obtener vino específico",
    description="Obtiene la información completa de un vino específico incluyendo bodega, denominación de origen, uvas y características.",
    response_description="Información detallada del vino"
)
def obtener_vino_publico(
    vino_id: int,
    service: VinoService = Depends(get_vino_service)
):
    """Obtiene un vino específico por ID"""
    vino = service.obtener_vino(vino_id)
    if not vino:
        raise HTTPException(status_code=404, detail="Vino no encontrado")
    
    return VinoResponse.model_validate(vino)

# ==================== CATEGORÍAS DE PLATOS ====================

@router.get(
    "/categorias-platos",
    response_model=List[CategoriaOut],
    summary="📂 Obtener categorías de platos",
    description="Lista todas las categorías de platos activas disponibles públicamente.",
    response_description="Lista de categorías de platos activas"
)
def get_categorias_platos_publicas(
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener todas las categorías de platos activas"""
    try:
        categorias = db.query(CategoriaPlato).filter(
            CategoriaPlato.is_active == True,
            CategoriaPlato.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
        return categorias
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías: {str(e)}")

# ==================== ALÉRGENOS ====================

@router.get(
    "/alergenos",
    response_model=List[AlerganoOut],
    summary="🚨 Obtener alérgenos",
    description="Lista todos los alérgenos registrados en el sistema.",
    response_description="Lista completa de alérgenos"
)
def get_alergenos_publicos(
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener todos los alérgenos"""
    try:
        alergenos = db.query(Alergeno).filter(
            Alergeno.is_active == True,
            Alergeno.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
        return alergenos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alérgenos: {str(e)}")

# ==================== CATEGORÍAS DE VINOS ====================

@router.get(
    "/categorias-vinos",
    response_model=List[CategoriaVinoOut],
    summary="🍷 Obtener categorías de vinos",
    description="Lista todas las categorías de vinos activas disponibles públicamente.",
    response_description="Lista de categorías de vinos activas"
)
def get_categorias_vinos_publicas(
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener todas las categorías de vinos activas"""
    try:
        categorias = db.query(CategoriaVino).filter(
            CategoriaVino.is_active == True,
            CategoriaVino.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
        return categorias
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías de vinos: {str(e)}")

# ==================== BODEGAS ====================

@router.get(
    "/bodegas",
    response_model=List[BodegaOut],
    summary="🏭 Obtener bodegas",
    description="Lista todas las bodegas activas registradas en el sistema.",
    response_description="Lista de bodegas activas"
)
def get_bodegas_publicas(
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener todas las bodegas activas"""
    try:
        bodegas = db.query(Bodega).filter(
            Bodega.is_active == True,
            Bodega.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
        return bodegas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener bodegas: {str(e)}")

# ==================== DENOMINACIONES DE ORIGEN ====================

@router.get(
    "/denominaciones-origen",
    response_model=List[DenominacionOrigenOut],
    summary="🏛️ Obtener denominaciones de origen",
    description="Lista todas las denominaciones de origen activas registradas.",
    response_description="Lista de denominaciones de origen activas"
)
def get_denominaciones_origen_publicas(
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener todas las denominaciones de origen activas"""
    try:
        denominaciones = db.query(DenominacionOrigen).filter(
            DenominacionOrigen.is_active == True,
            DenominacionOrigen.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
        return denominaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener denominaciones: {str(e)}")

# ==================== ENÓLOGOS ====================

@router.get(
    "/enologos",
    response_model=List[EnologoOut],
    summary="👨‍🔬 Obtener enólogos",
    description="Lista todos los enólogos activos registrados en el sistema.",
    response_description="Lista de enólogos activos"
)
def get_enologos_publicos(
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener todos los enólogos activos"""
    try:
        enologos = db.query(Enologo).filter(
            Enologo.is_active == True,
            Enologo.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
        return enologos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener enólogos: {str(e)}")

# ==================== UVAS ====================

@router.get(
    "/uvas",
    response_model=List[UvaOut],
    summary="🍇 Obtener tipos de uva",
    description="Lista todos los tipos de uva activos registrados en el sistema.",
    response_description="Lista de tipos de uva activos"
)
def get_uvas_publicas(
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener todos los tipos de uva activos"""
    try:
        uvas = db.query(Uva).filter(
            Uva.is_active == True,
            Uva.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
        return uvas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tipos de uva: {str(e)}")

# ==================== ENDPOINTS DE BÚSQUEDA ====================

@router.get(
    "/search/categorias-platos",
    response_model=List[CategoriaOut],
    summary="🔍 Buscar categorías de platos",
    description="Busca categorías de platos por nombre o descripción.",
    response_description="Categorías que coinciden con la búsqueda"
)
def search_categorias_platos(
    q: str = Query(..., min_length=2, description="Término de búsqueda"),
    limit: int = Query(20, ge=1, le=50, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Buscar categorías de platos por término"""
    try:
        categorias = db.query(CategoriaPlato).filter(
            CategoriaPlato.is_active == True,
            CategoriaPlato.deleted_at.is_(None),
            CategoriaPlato.nombre.ilike(f"%{q}%")
        ).limit(limit).all()
        return categorias
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@router.get(
    "/search/bodegas",
    response_model=List[BodegaOut],
    summary="🔍 Buscar bodegas",
    description="Busca bodegas por nombre, región o país.",
    response_description="Bodegas que coinciden con la búsqueda"
)
def search_bodegas(
    q: str = Query(..., min_length=2, description="Término de búsqueda"),
    limit: int = Query(20, ge=1, le=50, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Buscar bodegas por término"""
    try:
        bodegas = db.query(Bodega).filter(
            Bodega.is_active == True,
            Bodega.deleted_at.is_(None),
            (Bodega.nombre.ilike(f"%{q}%") | 
             Bodega.region.ilike(f"%{q}%") | 
             Bodega.pais.ilike(f"%{q}%"))
        ).limit(limit).all()
        return bodegas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")
