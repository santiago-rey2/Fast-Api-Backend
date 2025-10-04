"""
Repository para manejar queries de vinos
"""
from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_
from src.entities.vino import Vino
from src.entities.categoria_vino import CategoriaVino
from src.entities.denominacion_origen import DenominacionOrigen
from src.entities.bodega import Bodega

class VinosRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_vinos_with_filters(
        self,
        tipo: Optional[str] = None,
        denominacion: Optional[str] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None,
        incluir_inactivos: bool = False
    ) -> List[Vino]:
        """
        SOLO query - devuelve lista de objetos Vino
        """
        # Construir query base
        query = (
            self.db.query(Vino)
            .join(CategoriaVino)
            .outerjoin(DenominacionOrigen)  # outerjoin para vinos sin denominación
            .join(Bodega)
            .options(
                selectinload(Vino.uvas),
                selectinload(Vino.enologo)
            )
        )
        
        # Aplicar filtros básicos
        filters = []
        
        # Filtro por estado activo (por defecto solo activos)
        if not incluir_inactivos:
            filters.append(Vino.is_active == True)

        if tipo:
            filters.append(CategoriaVino.nombre.ilike(f"%{tipo}%"))
        
        if denominacion:
            filters.append(DenominacionOrigen.nombre.ilike(f"%{denominacion}%"))
        
        if precio_min is not None:
            filters.append(Vino.precio >= precio_min)
        
        if precio_max is not None:
            filters.append(Vino.precio <= precio_max)
        
        if filters:
            query = query.filter(and_(*filters))
        
        return query.order_by(CategoriaVino.nombre, DenominacionOrigen.nombre, Bodega.nombre).all()