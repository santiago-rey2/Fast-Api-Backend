"""
Repository para operaciones CRUD de Platos
"""
from typing import Sequence, Optional, List
from decimal import Decimal
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from src.entities.plato import Plato
from src.entities.alergeno import Alergeno
from src.entities.categoria_plato import CategoriaPlato

class PlatoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self, 
        categoria_id: Optional[int] = None,
        q: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        ordenar_por: str = "nombre"
    ) -> Sequence[Plato]:
        """Lista platos con filtros opcionales"""
        stmt = select(Plato).options(
            selectinload(Plato.categoria),
            selectinload(Plato.alergenos)
        )
        
        if categoria_id is not None:
            stmt = stmt.where(Plato.categoria_id == categoria_id)
        
        if q:
            stmt = stmt.where(Plato.nombre.like(f"%{q}%"))
        
        if ordenar_por == "precio":
            stmt = stmt.order_by(Plato.precio.asc())
        else:
            stmt = stmt.order_by(Plato.nombre.asc())
        
        return self.db.execute(
            stmt.offset(offset).limit(limit)
        ).scalars().all()

    def get_by_id(self, plato_id: int) -> Optional[Plato]:
        """Obtiene un plato por ID"""
        stmt = select(Plato).options(
            selectinload(Plato.categoria),
            selectinload(Plato.alergenos)
        ).where(Plato.id == plato_id)
        
        return self.db.execute(stmt).scalar_one_or_none()

    def create(
        self, 
        nombre: str, 
        precio: Decimal, 
        descripcion: Optional[str], 
        categoria_id: int,
        alergenos_ids: List[int]
    ) -> Plato:
        """Crea un nuevo plato"""
        plato = Plato(
            nombre=nombre, 
            precio=precio, 
            descripcion=descripcion, 
            categoria_id=categoria_id
        )
        
        if alergenos_ids:
            alergenos = self.db.execute(
                select(Alergeno).where(Alergeno.id.in_(alergenos_ids))
            ).scalars().all()
            plato.alergenos = list(alergenos)
        
        self.db.add(plato)
        self.db.commit()
        self.db.refresh(plato)
        return plato

    def update(
        self, 
        plato_id: int,
        nombre: Optional[str] = None,
        precio: Optional[Decimal] = None,
        descripcion: Optional[str] = None,
        categoria_id: Optional[int] = None,
        alergenos_ids: Optional[List[int]] = None
    ) -> Optional[Plato]:
        """Actualiza un plato existente"""
        plato = self.get_by_id(plato_id)
        if not plato:
            return None
        
        if nombre is not None:
            plato.nombre = nombre
        if precio is not None:
            plato.precio = precio
        if descripcion is not None:
            plato.descripcion = descripcion
        if categoria_id is not None:
            plato.categoria_id = categoria_id
        if alergenos_ids is not None:
            alergenos = self.db.execute(
                select(Alergeno).where(Alergeno.id.in_(alergenos_ids))
            ).scalars().all()
            plato.alergenos = list(alergenos)
        
        self.db.commit()
        self.db.refresh(plato)
        return plato

    def delete(self, plato_id: int) -> bool:
        """Elimina un plato"""
        plato = self.get_by_id(plato_id)
        if not plato:
            return False
        
        self.db.delete(plato)
        self.db.commit()
        return True

    def count(
        self, 
        categoria_id: Optional[int] = None,
        q: Optional[str] = None
    ) -> int:
        """Cuenta platos con filtros"""
        stmt = select(Plato)
        
        if categoria_id is not None:
            stmt = stmt.where(Plato.categoria_id == categoria_id)
        if q:
            stmt = stmt.where(Plato.nombre.like(f"%{q}%"))
        
        result = self.db.execute(
            select(Plato).where(stmt.whereclause if stmt.whereclause is not None else True)
        )
        return len(result.scalars().all())
