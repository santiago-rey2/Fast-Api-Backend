"""
Entidad PlatoTraduccion para gestionar las traducciones de los nombres de los platos.
"""
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class PlatoTraduccion(Base):
    __tablename__ = "plato_traducciones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    plato_id: Mapped[int] = mapped_column(ForeignKey("platos.id", ondelete="CASCADE"))
    idioma: Mapped[str] = mapped_column(String(5), index=True)  # ej: "es", "en", "fr"
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str] = mapped_column(Text)

    plato: Mapped["Plato"] = relationship(back_populates="traducciones")
