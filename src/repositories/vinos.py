"""
Repository para operaciones CRUD de Vinos
"""
from typing import Sequence, Optional, List
from decimal import Decimal
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from src.entities.vino import Vino
from src.entities.uva import Uva

class VinoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self, 
        categoria_id: Optional[int] = None,
        bodega_id: Optional[int] = None,
        q: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        ordenar_por: str = "nombre"
    ) -> Sequence[Vino]:
        """Lista vinos con filtros opcionales"""
        stmt = select(Vino).options(
            selectinload(Vino.categoria),
            selectinload(Vino.bodega),
            selectinload(Vino.denominacion_origen),
            selectinload(Vino.enologo),
            selectinload(Vino.uvas)
        )
        
        if categoria_id is not None:
            stmt = stmt.where(Vino.categoria_id == categoria_id)
        
        if bodega_id is not None:
            stmt = stmt.where(Vino.bodega_id == bodega_id)
        
        if q:
            stmt = stmt.where(Vino.nombre.like(f"%{q}%"))
        
        if ordenar_por == "precio":
            stmt = stmt.order_by(Vino.precio.asc())
        else:
            stmt = stmt.order_by(Vino.nombre.asc())
        
        return self.db.execute(
            stmt.offset(offset).limit(limit)
        ).scalars().all()

    def count(
        self, 
        categoria_id: Optional[int] = None,
        bodega_id: Optional[int] = None,
        q: Optional[str] = None
    ) -> int:
        """Cuenta el total de vinos con filtros"""
        stmt = select(func.count(Vino.id))
        
        if categoria_id is not None:
            stmt = stmt.where(Vino.categoria_id == categoria_id)
        
        if bodega_id is not None:
            stmt = stmt.where(Vino.bodega_id == bodega_id)
        
        if q:
            stmt = stmt.where(Vino.nombre.like(f"%{q}%"))
        
        return self.db.execute(stmt).scalar() or 0

    def get_by_id(self, vino_id: int) -> Optional[Vino]:
        """Obtiene un vino por ID"""
        stmt = select(Vino).options(
            selectinload(Vino.categoria),
            selectinload(Vino.bodega),
            selectinload(Vino.denominacion_origen),
            selectinload(Vino.enologo),
            selectinload(Vino.uvas)
        ).where(Vino.id == vino_id)
        
        return self.db.execute(stmt).scalar_one_or_none()

    def create(
        self, 
        nombre: str, 
        precio: Decimal, 
        categoria_id: int,
        bodega_id: Optional[int] = None,
        denominacion_origen_id: Optional[int] = None,
        enologo_id: Optional[int] = None,
        uvas_ids: List[int] = []
    ) -> Vino:
        """Crea un nuevo vino"""
        vino = Vino(
            nombre=nombre, 
            precio=precio, 
            categoria_id=categoria_id,
            bodega_id=bodega_id,
            denominacion_origen_id=denominacion_origen_id,
            enologo_id=enologo_id
        )
        
        if uvas_ids:
            uvas = self.db.execute(
                select(Uva).where(Uva.id.in_(uvas_ids))
            ).scalars().all()
            vino.uvas = list(uvas)
        
        self.db.add(vino)
        self.db.commit()
        self.db.refresh(vino)
        return vino

    def update(
        self, 
        vino_id: int,
        nombre: Optional[str] = None,
        precio: Optional[Decimal] = None,
        categoria_id: Optional[int] = None,
        bodega_id: Optional[int] = None,
        denominacion_origen_id: Optional[int] = None,
        enologo_id: Optional[int] = None,
        uvas_ids: Optional[List[int]] = None
    ) -> Optional[Vino]:
        """Actualiza un vino existente"""
        vino = self.get_by_id(vino_id)
        if not vino:
            return None
        
        if nombre is not None:
            vino.nombre = nombre
        if precio is not None:
            vino.precio = precio
        if categoria_id is not None:
            vino.categoria_id = categoria_id
        if bodega_id is not None:
            vino.bodega_id = bodega_id
        if denominacion_origen_id is not None:
            vino.denominacion_origen_id = denominacion_origen_id
        if enologo_id is not None:
            vino.enologo_id = enologo_id
        if uvas_ids is not None:
            uvas = self.db.execute(
                select(Uva).where(Uva.id.in_(uvas_ids))
            ).scalars().all()
            vino.uvas = list(uvas)
        
        self.db.commit()
        self.db.refresh(vino)
        return vino

    def delete(self, vino_id: int) -> bool:
        """Elimina un vino"""
        vino = self.get_by_id(vino_id)
        if not vino:
            return False
        
        self.db.delete(vino)
        self.db.commit()
        return True
