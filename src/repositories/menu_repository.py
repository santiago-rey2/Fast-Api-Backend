"""
Repository para manejar queries de menú
"""
from typing import List, Optional
from sqlalchemy.orm import Session, selectinload,contains_eager, with_loader_criteria 
from sqlalchemy import and_
from src.entities.plato import Plato
from src.entities.categoria_plato import CategoriaPlato
from src.entities.plato_traduccion import PlatoTraduccion

class MenuRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_platos_with_filters(
        self,
        idioma: str,
        categoria: Optional[str] = None,
        sugerencias: Optional[bool] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None,
        is_active: Optional[bool] = None
    ) -> List[Plato]:
        """
        SOLO query - devuelve lista de objetos Plato
        """
        # Construir query base
        query = (
            self.db.query(Plato)
            .join(Plato.traducciones)
            .join(CategoriaPlato)
            .options(
                contains_eager(Plato.traducciones),
                selectinload(Plato.alergenos),
                with_loader_criteria(PlatoTraduccion, PlatoTraduccion.idioma == idioma)
            )
            .filter(PlatoTraduccion.idioma == idioma)
        )
        
        # Aplicar filtros básicos
        filters = []
        
        if categoria:
            filters.append(CategoriaPlato.nombre.ilike(f"%{categoria}%"))
        
        if precio_min is not None:
            filters.append(Plato.precio >= precio_min)
        
        if precio_max is not None:
            filters.append(Plato.precio <= precio_max)

        if sugerencias is not None:
            filters.append(Plato.sugerencias == sugerencias)
            
        if is_active is not None:
            filters.append(Plato.is_active == is_active)
        
        if filters:
            query = query.filter(and_(*filters))
        
        return query.all()  # Devuelve objetos Plato, NO diccionarios