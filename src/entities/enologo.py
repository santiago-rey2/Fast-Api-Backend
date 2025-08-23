"""
Enólogos de vinos (campo nullable)
"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if TYPE_CHECKING:
    from src.entities.vino import Vino

class Enologo(Base):
    __tablename__ = "enologos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    experiencia_anos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Relationships
    vinos: Mapped[List["Vino"]] = relationship(
        "Vino", 
        back_populates="enologo"
    )
