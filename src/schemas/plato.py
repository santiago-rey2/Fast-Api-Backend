"""
Schemas Pydantic v2 para Platos
"""
from decimal import Decimal
from typing import Annotated, Optional, List
from pydantic import BaseModel, Field

# Type alias para precio con validación
Price = Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]

class AlerganoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=50)]

class AlerganoOut(AlerganoBase):
    id: int
    model_config = {"from_attributes": True}

class CategoriaBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=50)]

class CategoriaOut(CategoriaBase):
    id: int
    model_config = {"from_attributes": True}

class PlatoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=100)]
    precio: Price
    descripcion: Optional[str] = None
    categoria_id: int

class PlatoCreate(PlatoBase):
    alergenos_ids: List[int] = []

class PlatoUpdate(BaseModel):
    nombre: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    precio: Optional[Price] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    alergenos_ids: Optional[List[int]] = None

class PlatoOut(PlatoBase):
    id: int
    categoria: CategoriaOut
    alergenos: List[AlerganoOut] = []
    
    model_config = {"from_attributes": True}

# Alias para compatibilidad con las rutas
PlatoResponse = PlatoOut

class PlatosListResponse(BaseModel):
    """Respuesta paginada para lista de platos"""
    platos: List[PlatoResponse]
    total: int
    limit: int
    offset: int
