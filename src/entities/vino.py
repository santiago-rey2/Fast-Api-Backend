"""
Vinos del restaurante con relaciones múltiples
"""
from __future__ import annotations
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import String, Numeric, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.entities.bodega import Bodega
from src.entities.categoria_vino import CategoriaVino
from src.entities.denominacion_origen import DenominacionOrigen
from src.entities.enologo import Enologo
from src.entities.mixins import AuditMixin
from src.entities.uva import Uva

# Tabla intermedia para relación many-to-many entre vinos y uvas
vinos_uvas = Table(
    "vinos_uvas",
    Base.metadata,
    Column("vino_id", ForeignKey("vinos.id"), primary_key=True),
    Column("uva_id", ForeignKey("uvas.id"), primary_key=True),
)

class Vino(Base, AuditMixin):
    __tablename__ = "vinos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), index=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    precio_unidad: Mapped[Optional[str]] = mapped_column( String(20),nullable=True)
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categoria_vinos.id"), 
        index=True
    )
    
    # Foreign keys opcionales (nullable)
    bodega_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bodegas.id"), 
        nullable=True,
        index=True
    )
    denominacion_origen_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("denominaciones_origen.id"), 
        nullable=True,
        index=True
    )
    enologo_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("enologos.id"), 
        nullable=True,
        index=True
    )

    # Relationships
    categoria: Mapped["CategoriaVino"] = relationship(
        "CategoriaVino", 
        back_populates="vinos"
    )
    bodega: Mapped[Optional["Bodega"]] = relationship(
        "Bodega", 
        back_populates="vinos"
    )
    denominacion_origen: Mapped[Optional["DenominacionOrigen"]] = relationship(
        "DenominacionOrigen", 
        back_populates="vinos"
    )
    enologo: Mapped[Optional["Enologo"]] = relationship(
        "Enologo", 
        back_populates="vinos"
    )
    uvas: Mapped[List["Uva"]] = relationship(
        secondary=vinos_uvas, 
        back_populates="vinos"
    )
