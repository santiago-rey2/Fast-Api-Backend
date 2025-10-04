"""
Schemas para la documentación de la API de menú
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class VinoResponse(BaseModel):
    """Modelo de respuesta para un vino"""
    id: int = Field(..., description="ID único del vino")
    nombre: str = Field(..., description="Nombre del vino")
    precio: Optional[float] = Field(None, description="Precio del vino en euros")
    precio_unidad: Optional[str] = Field(None, description="Unidad del precio, e.g., 'ración', 'Kg'")
    bodega: str = Field(..., description="Nombre de la bodega")
    uvas: List[str] = Field(default_factory=list, description="Variedades de uva")
    enologo: Optional[str] = Field(None, description="Nombre del enólogo")

class VinosGroupedResponse(BaseModel):
    """Modelo de respuesta para vinos agrupados"""
    vinos: Dict[str, Dict[str, List[VinoResponse]]] = Field(
        ..., 
        description="Vinos agrupados por tipo y denominación de origen"
    )