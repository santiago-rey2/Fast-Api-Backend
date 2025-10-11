from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.services.menu_service import MenuService
from src.services.vinos_service import VinosService
from src.schemas.menu_schema import PlatosGroupedResponse
from src.schemas.wines_schema import VinosGroupedResponse

router = APIRouter(prefix="/public", tags=["Public"])

@router.get(
    "/platos",
    response_model=PlatosGroupedResponse,
    summary="Obtener platos agrupados por categoría",
    description="Devuelve todos los platos agrupados por categoría con filtros opcionales"
)
async def get_platos(
    db: Session = Depends(get_db),
    idioma: str = Query(
        ...,
        description="Idioma para las traducciones de los platos",
        example="es"
    ),
    categoria: Optional[str] = Query(
        None, 
        description="Filtrar por categoría específica (búsqueda parcial)",
        example="Entrantes"
    ),
    sugerencias: Optional[bool] = Query(
        None,
        description="Filtrar Solo sugerencías (búsqueda parcial)",
        example=True
    ),
    precio_min: Optional[float] = Query(
        None, 
        ge=0,
        description="Precio mínimo en euros",
        example=5.0
    ),
    precio_max: Optional[float] = Query(
        None, 
        ge=0,
        description="Precio máximo en euros",
        example=25.0
    )
):
    """
    Obtiene todos los platos agrupados por categoría.
    
    **Parámetros de filtrado:**
    - **categoria**: Busca categorías que contengan este texto
    - **precio_min**: Filtra platos con precio mayor o igual
    - **precio_max**: Filtra platos con precio menor o igual
    
    **Estructura de respuesta:**
    ```json
    {
      "platos": {
        "Entrantes": [
          {
            "id": 1,
            "nombre": "Ensalada César",
            "descripcion": "...",
            "precio": 12.50,
            "alergenos": ["Gluten", "Huevos"]
          }
        ]
      }
    }
    ```
    """
    try:
        menu_repo = MenuService(db)
        platos_agrupados = menu_repo.get_platos_public(
            idioma=idioma,
            categoria=categoria,
            sugerencias=sugerencias,
            precio_min=precio_min,
            precio_max=precio_max
        )
        return {"platos": platos_agrupados}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener platos: {str(e)}")

@router.get(
    "/vinos",
    response_model=VinosGroupedResponse,
    summary="Obtener vinos agrupados por tipo y denominación",
    description="Devuelve todos los vinos agrupados por tipo y denominación de origen con filtros opcionales"
)
async def get_vinos(
    db: Session = Depends(get_db),
    tipo: Optional[str] = Query(
        None,
        description="Filtrar por tipo de vino (búsqueda parcial)",
        example="Tinto"
    ),
    denominacion: Optional[str] = Query(
        None,
        description="Filtrar por denominación de origen (búsqueda parcial)",
        example="Rioja"
    ),
    precio_min: Optional[float] = Query(
        None,
        ge=0,
        description="Precio mínimo en euros",
        example=10.0
    ),
    precio_max: Optional[float] = Query(
        None,
        ge=0,
        description="Precio máximo en euros",
        example=50.0
    )
):
    """
    Obtiene todos los vinos agrupados por tipo y denominación de origen.
    
    **Parámetros de filtrado:**
    - **tipo**: Busca tipos que contengan este texto (Tinto, Blanco, etc.)
    - **denominacion**: Busca denominaciones que contengan este texto
    - **precio_min**: Filtra vinos con precio mayor o igual
    - **precio_max**: Filtra vinos con precio menor o igual
    
    **Estructura de respuesta:**
    ```json
    {
      "vinos": {
        "Tinto joven": {
          "D.O. Rioja": [
            {
              "id": 1,
              "nombre": "Marqués de Riscal Reserva",
              "precio": 15.90,
              "bodega": "Marqués de Riscal",
              "uvas": ["Tempranillo"],
              "enologo": "Francisco Hurtado"
            }
          ]
        }
      }
    }
    ```
    """
    try:
        vinos_service = VinosService(db)
        vinos_agrupados = vinos_service.get_vinos_public(
            tipo=tipo,
            denominacion=denominacion,
            precio_min=precio_min,
            precio_max=precio_max
        )
        return {"vinos": vinos_agrupados}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener vinos: {str(e)}")
