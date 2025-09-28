"""
Schemas para la documentación de la API de menú
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class PlatoResponse(BaseModel):
    """Modelo de respuesta para un plato"""
    id: int = Field(..., description="ID único del plato")
    nombre: str = Field(..., description="Nombre del plato")
    descripcion: Optional[str] = Field(None, description="Descripción del plato")
    precio: Optional[float] = Field(None, description="Precio del plato en euros")
    alergenos: List[str] = Field(default_factory=list, description="Lista de alérgenos")

class PlatosGroupedResponse(BaseModel):
    """Modelo de respuesta para platos agrupados"""
    platos: Dict[str, List[PlatoResponse]] = Field(..., description="Platos agrupados por categoría")
