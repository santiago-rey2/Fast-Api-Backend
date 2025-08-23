"""
Categorías de vinos
"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.entities.mixins import AuditMixin

if TYPE_CHECKING:
    from src.entities.vino import Vino

class CategoriaVino(Base, AuditMixin):
    __tablename__ = "categoria_vinos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    # Relationships
    vinos: Mapped[List["Vino"]] = relationship(
        "Vino", 
        back_populates="categoria"
    )
