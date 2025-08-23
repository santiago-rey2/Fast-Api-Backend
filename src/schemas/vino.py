"""
Schemas Pydantic v2 para Vinos
"""
from decimal import Decimal
from typing import Annotated, Optional, List
from pydantic import BaseModel, Field

# Type alias para precio con validación
Price = Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]

class BodegaBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=100)]

class BodegaOut(BodegaBase):
    id: int
    model_config = {"from_attributes": True}

class DenominacionOrigenBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=100)]

class DenominacionOrigenOut(DenominacionOrigenBase):
    id: int
    model_config = {"from_attributes": True}

class EnologoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=100)]

class EnologoOut(EnologoBase):
    id: int
    model_config = {"from_attributes": True}

class UvaBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=50)]

class UvaOut(UvaBase):
    id: int
    model_config = {"from_attributes": True}

class CategoriaVinoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=50)]

class CategoriaVinoOut(CategoriaVinoBase):
    id: int
    model_config = {"from_attributes": True}

class VinoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=100)]
    precio: Price
    categoria_id: int
    bodega_id: Optional[int] = None
    denominacion_origen_id: Optional[int] = None
    enologo_id: Optional[int] = None

class VinoCreate(VinoBase):
    uvas_ids: List[int] = []

class VinoUpdate(BaseModel):
    nombre: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    precio: Optional[Price] = None
    categoria_id: Optional[int] = None
    bodega_id: Optional[int] = None
    denominacion_origen_id: Optional[int] = None
    enologo_id: Optional[int] = None
    uvas_ids: Optional[List[int]] = None

class VinoOut(VinoBase):
    id: int
    categoria: CategoriaVinoOut
    bodega: Optional[BodegaOut] = None
    denominacion_origen: Optional[DenominacionOrigenOut] = None
    enologo: Optional[EnologoOut] = None
    uvas: List[UvaOut] = []
    
    model_config = {"from_attributes": True}

# Alias para compatibilidad con las rutas
VinoResponse = VinoOut

class VinosListResponse(BaseModel):
    """Respuesta paginada para lista de vinos"""
    vinos: List[VinoResponse]
    total: int
    limit: int
    offset: int
