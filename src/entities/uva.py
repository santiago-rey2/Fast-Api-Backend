"""
Tipos de uva para vinos
"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.entities.mixins import AuditMixin

if TYPE_CHECKING:
    from src.entities.vino import Vino

class Uva(Base, AuditMixin):
    __tablename__ = "uvas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    tipo: Mapped[str] = mapped_column(String(20), default="sin especificar", nullable=False)
    
    # Relationships
    vinos: Mapped[List["Vino"]] = relationship(
        secondary="vinos_uvas", 
        back_populates="uvas"
    )
