"""
Bodegas de vinos (campo nullable)
"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.entities.mixins import AuditMixin

if TYPE_CHECKING:
    from src.entities.vino import Vino

class Bodega(Base, AuditMixin):
    __tablename__ = "bodegas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    region: Mapped[str] = mapped_column(String(100), default="sin especificar", nullable=False)
    
    # Relationships
    vinos: Mapped[List["Vino"]] = relationship(
        "Vino", 
        back_populates="bodega"
    )
