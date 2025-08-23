"""
Rutas de administración para gestionar entidades del sistema
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..entities.categoria_plato import CategoriaPlato as Categoria
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

router = APIRouter(prefix="/admin", tags=["Administración"])

# ==================== CATEGORÍAS DE PLATOS ====================

@router.get("/categorias", response_model=List[CategoriaOut])
def get_categorias(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todas las categorías de platos"""
    categorias = db.query(Categoria).offset(skip).limit(limit).all()
    return categorias

@router.post("/categorias", response_model=CategoriaOut)
def create_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva categoría de platos"""
    # Verificar si ya existe
    existing = db.query(Categoria).filter(Categoria.nombre == categoria.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    
    db_categoria = Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.put("/categorias/{categoria_id}", response_model=CategoriaOut)
def update_categoria(
    categoria_id: int,
    categoria: CategoriaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una categoría de platos"""
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    for field, value in categoria.model_dump(exclude_unset=True).items():
        setattr(db_categoria, field, value)
    
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.delete("/categorias/{categoria_id}")
def delete_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar una categoría de platos"""
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db.delete(db_categoria)
    db.commit()
    return {"message": "Categoría eliminada correctamente"}

# ==================== ALÉRGENOS ====================

@router.get("/alergenos", response_model=List[AlerganoOut])
def get_alergenos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los alérgenos"""
    alergenos = db.query(Alergeno).offset(skip).limit(limit).all()
    return alergenos

@router.post("/alergenos", response_model=AlerganoOut)
def create_alergeno(
    alergeno: AlerganoCreate,
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

@router.put("/alergenos/{alergeno_id}", response_model=AlerganoOut)
def update_alergeno(
    alergeno_id: int,
    alergeno: AlerganoUpdate,
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

@router.delete("/alergenos/{alergeno_id}")
def delete_alergeno(
    alergeno_id: int,
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

@router.get("/categorias-vinos", response_model=List[CategoriaVinoOut])
def get_categorias_vinos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todas las categorías de vinos"""
    categorias = db.query(CategoriaVino).offset(skip).limit(limit).all()
    return categorias

@router.post("/categorias-vinos", response_model=CategoriaVinoOut)
def create_categoria_vino(
    categoria: CategoriaVinoCreate,
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

@router.put("/categorias-vinos/{categoria_id}", response_model=CategoriaVinoOut)
def update_categoria_vino(
    categoria_id: int,
    categoria: CategoriaVinoUpdate,
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

@router.delete("/categorias-vinos/{categoria_id}")
def delete_categoria_vino(
    categoria_id: int,
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

@router.get("/bodegas", response_model=List[BodegaOut])
def get_bodegas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todas las bodegas"""
    bodegas = db.query(Bodega).offset(skip).limit(limit).all()
    return bodegas

@router.post("/bodegas", response_model=BodegaOut)
def create_bodega(
    bodega: BodegaCreate,
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

@router.put("/bodegas/{bodega_id}", response_model=BodegaOut)
def update_bodega(
    bodega_id: int,
    bodega: BodegaUpdate,
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

@router.delete("/bodegas/{bodega_id}")
def delete_bodega(
    bodega_id: int,
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

@router.get("/denominaciones-origen", response_model=List[DenominacionOrigenOut])
def get_denominaciones_origen(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todas las denominaciones de origen"""
    denominaciones = db.query(DenominacionOrigen).offset(skip).limit(limit).all()
    return denominaciones

@router.post("/denominaciones-origen", response_model=DenominacionOrigenOut)
def create_denominacion_origen(
    denominacion: DenominacionOrigenCreate,
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

@router.put("/denominaciones-origen/{denominacion_id}", response_model=DenominacionOrigenOut)
def update_denominacion_origen(
    denominacion_id: int,
    denominacion: DenominacionOrigenUpdate,
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

@router.delete("/denominaciones-origen/{denominacion_id}")
def delete_denominacion_origen(
    denominacion_id: int,
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

@router.get("/enologos", response_model=List[EnologoOut])
def get_enologos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los enólogos"""
    enologos = db.query(Enologo).offset(skip).limit(limit).all()
    return enologos

@router.post("/enologos", response_model=EnologoOut)
def create_enologo(
    enologo: EnologoCreate,
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

@router.put("/enologos/{enologo_id}", response_model=EnologoOut)
def update_enologo(
    enologo_id: int,
    enologo: EnologoUpdate,
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

@router.delete("/enologos/{enologo_id}")
def delete_enologo(
    enologo_id: int,
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

@router.get("/uvas", response_model=List[UvaOut])
def get_uvas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todas las uvas"""
    uvas = db.query(Uva).offset(skip).limit(limit).all()
    return uvas

@router.post("/uvas", response_model=UvaOut)
def create_uva(
    uva: UvaCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva uva"""
    existing = db.query(Uva).filter(Uva.nombre == uva.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="La uva ya existe")
    
    db_uva = Uva(**uva.model_dump())
    db.add(db_uva)
    db.commit()
    db.refresh(db_uva)
    return db_uva

@router.put("/uvas/{uva_id}", response_model=UvaOut)
def update_uva(
    uva_id: int,
    uva: UvaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una uva"""
    db_uva = db.query(Uva).filter(Uva.id == uva_id).first()
    if not db_uva:
        raise HTTPException(status_code=404, detail="Uva no encontrada")
    
    for field, value in uva.model_dump(exclude_unset=True).items():
        setattr(db_uva, field, value)
    
    db.commit()
    db.refresh(db_uva)
    return db_uva

@router.delete("/uvas/{uva_id}")
def delete_uva(
    uva_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar una uva"""
    db_uva = db.query(Uva).filter(Uva.id == uva_id).first()
    if not db_uva:
        raise HTTPException(status_code=404, detail="Uva no encontrada")
    
    db.delete(db_uva)
    db.commit()
    return {"message": "Uva eliminada correctamente"}

# ==================== FIN DE ADMINISTRACIÓN ====================
