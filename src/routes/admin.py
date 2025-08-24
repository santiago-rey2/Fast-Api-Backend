"""
Rutas de administración para gestionar entidades del sistema (configuración general)
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth.dependencies import get_current_admin_user
from ..entities.user import User
from ..entities.categoria_plato import CategoriaPlato
from ..entities.alergeno import Alergeno
from ..entities.categoria_vino import CategoriaVino
from ..entities.bodega import Bodega
from ..entities.denominacion_origen import DenominacionOrigen
from ..entities.enologo import Enologo
from ..entities.uva import Uva
from ..schemas.admin import (
    CategoriaCreate, CategoriaUpdate, CategoriaOut,
    AlerganoCreate, AlerganoUpdate, AlerganoOut,
    CategoriaVinoCreate, CategoriaVinoUpdate, CategoriaVinoOut,
    BodegaCreate, BodegaUpdate, BodegaOut,
    DenominacionOrigenCreate, DenominacionOrigenUpdate, DenominacionOrigenOut,
    EnologoCreate, EnologoUpdate, EnologoOut,
    UvaCreate, UvaUpdate, UvaOut
)

router = APIRouter(
    prefix="/admin", 
    tags=["🏗️ Administración - Configuración General"],
    dependencies=[Depends(get_current_admin_user)],
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Permisos de administrador requeridos"}
    }
)

# ==================== CATEGORÍAS DE PLATOS ====================

@router.get(
    "/categorias-platos", 
    response_model=List[CategoriaOut],
    summary="📂 Listar categorías de platos (admin)",
    description="Obtiene todas las categorías de platos para administración.",
    response_description="Lista de categorías de platos"
)
def get_categorias_platos_admin(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las categorías de platos para administración"""
    categorias = db.query(CategoriaPlato).offset(skip).limit(limit).all()
    return categorias

@router.post(
    "/categorias-platos", 
    response_model=CategoriaOut,
    summary="➕ Crear categoría de platos",
    description="Crea una nueva categoría de platos en el sistema.",
    response_description="Categoría creada exitosamente"
)
def create_categoria_platos(
    categoria: CategoriaCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva categoría de platos"""
    existing = db.query(CategoriaPlato).filter(CategoriaPlato.nombre == categoria.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    
    db_categoria = CategoriaPlato(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.put(
    "/categorias-platos/{categoria_id}", 
    response_model=CategoriaOut,
    summary="✏️ Actualizar categoría de platos",
    description="Actualiza una categoría de platos existente.",
    response_description="Categoría actualizada"
)
def update_categoria_platos(
    categoria_id: int,
    categoria: CategoriaUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Actualizar una categoría de platos"""
    db_categoria = db.query(CategoriaPlato).filter(CategoriaPlato.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    for field, value in categoria.model_dump(exclude_unset=True).items():
        setattr(db_categoria, field, value)
    
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.delete(
    "/categorias-platos/{categoria_id}",
    summary="🗑️ Eliminar categoría de platos",
    description="Elimina una categoría de platos del sistema.",
    response_description="Confirmación de eliminación"
)
def delete_categoria_platos(
    categoria_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Eliminar una categoría de platos"""
    db_categoria = db.query(CategoriaPlato).filter(CategoriaPlato.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db.delete(db_categoria)
    db.commit()
    return {"message": "Categoría eliminada correctamente"}

# ==================== ALÉRGENOS ====================

@router.get(
    "/alergenos", 
    response_model=List[AlerganoOut],
    summary="🚨 Listar alérgenos (admin)",
    description="Obtiene todos los alérgenos para administración.",
    response_description="Lista de alérgenos"
)
def get_alergenos_admin(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener todos los alérgenos para administración"""
    alergenos = db.query(Alergeno).offset(skip).limit(limit).all()
    return alergenos

@router.post(
    "/alergenos", 
    response_model=AlerganoOut,
    summary="➕ Crear alérgeno",
    description="Registra un nuevo alérgeno en el sistema.",
    response_description="Alérgeno creado exitosamente"
)
def create_alergeno(
    alergeno: AlerganoCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo alérgeno"""
    existing = db.query(Alergeno).filter(Alergeno.nombre == alergeno.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="El alérgeno ya existe")
    
    db_alergeno = Alergeno(**alergeno.model_dump())
    db.add(db_alergeno)
    db.commit()
    db.refresh(db_alergeno)
    return db_alergeno

@router.put(
    "/alergenos/{alergeno_id}", 
    response_model=AlerganoOut,
    summary="✏️ Actualizar alérgeno",
    description="Actualiza la información de un alérgeno existente.",
    response_description="Alérgeno actualizado"
)
def update_alergeno(
    alergeno_id: int,
    alergeno: AlerganoUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Actualizar un alérgeno"""
    db_alergeno = db.query(Alergeno).filter(Alergeno.id == alergeno_id).first()
    if not db_alergeno:
        raise HTTPException(status_code=404, detail="Alérgeno no encontrado")
    
    for field, value in alergeno.model_dump(exclude_unset=True).items():
        setattr(db_alergeno, field, value)
    
    db.commit()
    db.refresh(db_alergeno)
    return db_alergeno

@router.delete(
    "/alergenos/{alergeno_id}",
    summary="🗑️ Eliminar alérgeno",
    description="Elimina un alérgeno del sistema.",
    response_description="Confirmación de eliminación"
)
def delete_alergeno(
    alergeno_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Eliminar un alérgeno"""
    db_alergeno = db.query(Alergeno).filter(Alergeno.id == alergeno_id).first()
    if not db_alergeno:
        raise HTTPException(status_code=404, detail="Alérgeno no encontrado")
    
    db.delete(db_alergeno)
    db.commit()
    return {"message": "Alérgeno eliminado correctamente"}

# ==================== CATEGORÍAS DE VINOS ====================

@router.get(
    "/categorias-vinos", 
    response_model=List[CategoriaVinoOut],
    summary="🍇 Listar categorías de vinos",
    description="Obtiene todas las categorías de vinos disponibles en el sistema.",
    response_description="Lista de categorías de vinos"
)
def get_categorias_vinos(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las categorías de vinos"""
    categorias = db.query(CategoriaVino).offset(skip).limit(limit).all()
    return categorias

@router.post(
    "/categorias-vinos", 
    response_model=CategoriaVinoOut,
    summary="➕ Crear categoría de vino",
    description="Crea una nueva categoría de vinos en el sistema.",
    response_description="Categoría de vino creada exitosamente"
)
def create_categoria_vino(
    categoria: CategoriaVinoCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva categoría de vinos"""
    existing = db.query(CategoriaVino).filter(CategoriaVino.nombre == categoria.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="La categoría de vino ya existe")
    
    db_categoria = CategoriaVino(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.put(
    "/categorias-vinos/{categoria_id}", 
    response_model=CategoriaVinoOut,
    summary="✏️ Actualizar categoría de vino",
    description="Actualiza una categoría de vinos existente.",
    response_description="Categoría de vino actualizada"
)
def update_categoria_vino(
    categoria_id: int,
    categoria: CategoriaVinoUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Actualizar una categoría de vinos"""
    db_categoria = db.query(CategoriaVino).filter(CategoriaVino.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría de vino no encontrada")
    
    for field, value in categoria.model_dump(exclude_unset=True).items():
        setattr(db_categoria, field, value)
    
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.delete(
    "/categorias-vinos/{categoria_id}",
    summary="🗑️ Eliminar categoría de vino",
    description="Elimina una categoría de vinos del sistema.",
    response_description="Confirmación de eliminación"
)
def delete_categoria_vino(
    categoria_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Eliminar una categoría de vinos"""
    db_categoria = db.query(CategoriaVino).filter(CategoriaVino.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría de vino no encontrada")
    
    db.delete(db_categoria)
    db.commit()
    return {"message": "Categoría de vino eliminada correctamente"}

# ==================== BODEGAS ====================

@router.get(
    "/bodegas", 
    response_model=List[BodegaOut],
    summary="🏭 Listar bodegas",
    description="Obtiene todas las bodegas registradas en el sistema.",
    response_description="Lista de bodegas registradas"
)
def get_bodegas(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las bodegas"""
    bodegas = db.query(Bodega).offset(skip).limit(limit).all()
    return bodegas

@router.post(
    "/bodegas", 
    response_model=BodegaOut,
    summary="➕ Crear bodega",
    description="Registra una nueva bodega en el sistema.",
    response_description="Bodega creada exitosamente"
)
def create_bodega(
    bodega: BodegaCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva bodega"""
    existing = db.query(Bodega).filter(Bodega.nombre == bodega.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="La bodega ya existe")
    
    db_bodega = Bodega(**bodega.model_dump())
    db.add(db_bodega)
    db.commit()
    db.refresh(db_bodega)
    return db_bodega

@router.put(
    "/bodegas/{bodega_id}", 
    response_model=BodegaOut,
    summary="✏️ Actualizar bodega",
    description="Actualiza la información de una bodega existente.",
    response_description="Bodega actualizada"
)
def update_bodega(
    bodega_id: int,
    bodega: BodegaUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Actualizar una bodega"""
    db_bodega = db.query(Bodega).filter(Bodega.id == bodega_id).first()
    if not db_bodega:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    
    for field, value in bodega.model_dump(exclude_unset=True).items():
        setattr(db_bodega, field, value)
    
    db.commit()
    db.refresh(db_bodega)
    return db_bodega

@router.delete(
    "/bodegas/{bodega_id}",
    summary="🗑️ Eliminar bodega",
    description="Elimina una bodega del sistema.",
    response_description="Confirmación de eliminación"
)
def delete_bodega(
    bodega_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Eliminar una bodega"""
    db_bodega = db.query(Bodega).filter(Bodega.id == bodega_id).first()
    if not db_bodega:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    
    db.delete(db_bodega)
    db.commit()
    return {"message": "Bodega eliminada correctamente"}

# ==================== DENOMINACIONES DE ORIGEN ====================

@router.get(
    "/denominaciones-origen", 
    response_model=List[DenominacionOrigenOut],
    summary="🏛️ Listar denominaciones de origen",
    description="Obtiene todas las denominaciones de origen registradas.",
    response_description="Lista de denominaciones de origen"
)
def get_denominaciones_origen(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las denominaciones de origen"""
    denominaciones = db.query(DenominacionOrigen).offset(skip).limit(limit).all()
    return denominaciones

@router.post(
    "/denominaciones-origen", 
    response_model=DenominacionOrigenOut,
    summary="➕ Crear denominación de origen",
    description="Registra una nueva denominación de origen.",
    response_description="Denominación de origen creada"
)
def create_denominacion_origen(
    denominacion: DenominacionOrigenCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva denominación de origen"""
    existing = db.query(DenominacionOrigen).filter(DenominacionOrigen.nombre == denominacion.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="La denominación de origen ya existe")
    
    db_denominacion = DenominacionOrigen(**denominacion.model_dump())
    db.add(db_denominacion)
    db.commit()
    db.refresh(db_denominacion)
    return db_denominacion

@router.put(
    "/denominaciones-origen/{denominacion_id}", 
    response_model=DenominacionOrigenOut,
    summary="✏️ Actualizar denominación de origen",
    description="Actualiza una denominación de origen existente.",
    response_description="Denominación de origen actualizada"
)
def update_denominacion_origen(
    denominacion_id: int,
    denominacion: DenominacionOrigenUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Actualizar una denominación de origen"""
    db_denominacion = db.query(DenominacionOrigen).filter(DenominacionOrigen.id == denominacion_id).first()
    if not db_denominacion:
        raise HTTPException(status_code=404, detail="Denominación de origen no encontrada")
    
    for field, value in denominacion.model_dump(exclude_unset=True).items():
        setattr(db_denominacion, field, value)
    
    db.commit()
    db.refresh(db_denominacion)
    return db_denominacion

@router.delete(
    "/denominaciones-origen/{denominacion_id}",
    summary="🗑️ Eliminar denominación de origen",
    description="Elimina una denominación de origen del sistema.",
    response_description="Confirmación de eliminación"
)
def delete_denominacion_origen(
    denominacion_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Eliminar una denominación de origen"""
    db_denominacion = db.query(DenominacionOrigen).filter(DenominacionOrigen.id == denominacion_id).first()
    if not db_denominacion:
        raise HTTPException(status_code=404, detail="Denominación de origen no encontrada")
    
    db.delete(db_denominacion)
    db.commit()
    return {"message": "Denominación de origen eliminada correctamente"}

# ==================== ENÓLOGOS ====================

@router.get(
    "/enologos", 
    response_model=List[EnologoOut],
    summary="👨‍🔬 Listar enólogos",
    description="Obtiene todos los enólogos registrados en el sistema.",
    response_description="Lista de enólogos registrados"
)
def get_enologos(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener todos los enólogos"""
    enologos = db.query(Enologo).offset(skip).limit(limit).all()
    return enologos

@router.post(
    "/enologos", 
    response_model=EnologoOut,
    summary="➕ Crear enólogo",
    description="Registra un nuevo enólogo en el sistema.",
    response_description="Enólogo creado exitosamente"
)
def create_enologo(
    enologo: EnologoCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo enólogo"""
    existing = db.query(Enologo).filter(Enologo.nombre == enologo.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="El enólogo ya existe")
    
    db_enologo = Enologo(**enologo.model_dump())
    db.add(db_enologo)
    db.commit()
    db.refresh(db_enologo)
    return db_enologo

@router.put(
    "/enologos/{enologo_id}", 
    response_model=EnologoOut,
    summary="✏️ Actualizar enólogo",
    description="Actualiza la información de un enólogo existente.",
    response_description="Enólogo actualizado"
)
def update_enologo(
    enologo_id: int,
    enologo: EnologoUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Actualizar un enólogo"""
    db_enologo = db.query(Enologo).filter(Enologo.id == enologo_id).first()
    if not db_enologo:
        raise HTTPException(status_code=404, detail="Enólogo no encontrado")
    
    for field, value in enologo.model_dump(exclude_unset=True).items():
        setattr(db_enologo, field, value)
    
    db.commit()
    db.refresh(db_enologo)
    return db_enologo

@router.delete(
    "/enologos/{enologo_id}",
    summary="🗑️ Eliminar enólogo",
    description="Elimina un enólogo del sistema.",
    response_description="Confirmación de eliminación"
)
def delete_enologo(
    enologo_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Eliminar un enólogo"""
    db_enologo = db.query(Enologo).filter(Enologo.id == enologo_id).first()
    if not db_enologo:
        raise HTTPException(status_code=404, detail="Enólogo no encontrado")
    
    db.delete(db_enologo)
    db.commit()
    return {"message": "Enólogo eliminado correctamente"}

# ==================== UVAS ====================

@router.get(
    "/uvas", 
    response_model=List[UvaOut],
    summary="🍇 Listar tipos de uva",
    description="Obtiene todos los tipos de uva registrados en el sistema.",
    response_description="Lista de tipos de uva registrados"
)
def get_uvas(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Obtener todos los tipos de uva"""
    uvas = db.query(Uva).offset(skip).limit(limit).all()
    return uvas

@router.post(
    "/uvas", 
    response_model=UvaOut,
    summary="➕ Crear tipo de uva",
    description="Registra un nuevo tipo de uva en el sistema.",
    response_description="Tipo de uva creado exitosamente"
)
def create_uva(
    uva: UvaCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo tipo de uva"""
    existing = db.query(Uva).filter(Uva.nombre == uva.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="El tipo de uva ya existe")
    
    db_uva = Uva(**uva.model_dump())
    db.add(db_uva)
    db.commit()
    db.refresh(db_uva)
    return db_uva

@router.put(
    "/uvas/{uva_id}", 
    response_model=UvaOut,
    summary="✏️ Actualizar tipo de uva",
    description="Actualiza la información de un tipo de uva existente.",
    response_description="Tipo de uva actualizado"
)
def update_uva(
    uva_id: int,
    uva: UvaUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Actualizar un tipo de uva"""
    db_uva = db.query(Uva).filter(Uva.id == uva_id).first()
    if not db_uva:
        raise HTTPException(status_code=404, detail="Tipo de uva no encontrado")
    
    for field, value in uva.model_dump(exclude_unset=True).items():
        setattr(db_uva, field, value)
    
    db.commit()
    db.refresh(db_uva)
    return db_uva

@router.delete(
    "/uvas/{uva_id}",
    summary="🗑️ Eliminar tipo de uva",
    description="Elimina un tipo de uva del sistema.",
    response_description="Confirmación de eliminación"
)
def delete_uva(
    uva_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Eliminar un tipo de uva"""
    db_uva = db.query(Uva).filter(Uva.id == uva_id).first()
    if not db_uva:
        raise HTTPException(status_code=404, detail="Tipo de uva no encontrado")
    
    db.delete(db_uva)
    db.commit()
    return {"message": "Tipo de uva eliminado correctamente"}