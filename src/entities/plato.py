"""
Platos del restaurante con relaciones many-to-many con alérgenos
"""
from __future__ import annotations
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import String, Text, Numeric, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

# Tabla intermedia para relación many-to-many entre platos y alérgenos
platos_alergenos = Table(
    "platos_alergenos",
    Base.metadata,
    Column("plato_id", ForeignKey("platos.id"), primary_key=True),
    Column("alergeno_id", ForeignKey("alergenos.id"), primary_key=True),
)

class Plato(Base):
    __tablename__ = "platos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), index=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categoria_platos.id"), 
        index=True
    )

    # Relationships
    categoria: Mapped["CategoriaPlato"] = relationship(
        "CategoriaPlato", 
        back_populates="platos"
    )
    alergenos: Mapped[List["Alergeno"]] = relationship(
        secondary=platos_alergenos, 
        back_populates="platos"
    )
