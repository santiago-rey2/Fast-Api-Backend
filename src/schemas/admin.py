"""
Schemas Pydantic v2 para Administración del Sistema
"""
from typing import Annotated, Optional, List
from pydantic import BaseModel, Field

# ==================== CATEGORÍAS DE PLATOS ====================

class CategoriaBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=50)]

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None

class CategoriaOut(CategoriaBase):
    id: int
    model_config = {"from_attributes": True}

# ==================== ALÉRGENOS ====================

class AlerganoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=50)]

class AlerganoCreate(AlerganoBase):
    pass

class AlerganoUpdate(BaseModel):
    nombre: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None

class AlerganoOut(AlerganoBase):
    id: int
    model_config = {"from_attributes": True}

# ==================== CATEGORÍAS DE VINOS ====================

class CategoriaVinoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=50)]

class CategoriaVinoCreate(CategoriaVinoBase):
    pass

class CategoriaVinoUpdate(BaseModel):
    nombre: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None

class CategoriaVinoOut(CategoriaVinoBase):
    id: int
    model_config = {"from_attributes": True}

# ==================== BODEGAS ====================

class BodegaBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=100)]
    region: Annotated[str, Field(min_length=1, max_length=100)] = "sin especificar"

class BodegaCreate(BodegaBase):
    pass

class BodegaUpdate(BaseModel):
    nombre: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    region: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None

class BodegaOut(BodegaBase):
    id: int
    model_config = {"from_attributes": True}

# ==================== DENOMINACIONES DE ORIGEN ====================

class DenominacionOrigenBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=100)]
    region: Annotated[str, Field(min_length=1, max_length=100)] = "sin especificar"

class DenominacionOrigenCreate(DenominacionOrigenBase):
    pass

class DenominacionOrigenUpdate(BaseModel):
    nombre: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    region: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None

class DenominacionOrigenOut(DenominacionOrigenBase):
    id: int
    model_config = {"from_attributes": True}

# ==================== ENÓLOGOS ====================

class EnologoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=100)]
    experiencia_anos: Annotated[int, Field(ge=0)] = 0

class EnologoCreate(EnologoBase):
    pass

class EnologoUpdate(BaseModel):
    nombre: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    experiencia_anos: Optional[Annotated[int, Field(ge=0)]] = None

class EnologoOut(EnologoBase):
    id: int
    model_config = {"from_attributes": True}

# ==================== UVAS ====================

class UvaBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=50)]
    tipo: Annotated[str, Field(min_length=1, max_length=20)] = "sin especificar"

class UvaCreate(UvaBase):
    pass

class UvaUpdate(BaseModel):
    nombre: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None
    tipo: Optional[Annotated[str, Field(min_length=1, max_length=20)]] = None

class UvaOut(UvaBase):
    id: int
    model_config = {"from_attributes": True}
