"""
Alérgenos de los platos
"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if TYPE_CHECKING:
    from src.entities.plato import Plato

class Alergeno(Base):
    __tablename__ = "alergenos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    # Relationships
    platos: Mapped[List["Plato"]] = relationship(
        secondary="platos_alergenos", 
        back_populates="alergenos"
    )
