"""
Mixin base para campos de auditoría y control de estado
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

class AuditMixin:
    """
    Mixin que proporciona campos de auditoría y control de estado
    para todas las entidades del sistema
    """
    
    # Campos de auditoría temporal
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
        comment="Fecha y hora de creación del registro"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Fecha y hora de última modificación"
    )
    
    # Campos de control de estado
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Indica si el registro está activo"
    )
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Fecha y hora de eliminación lógica (soft delete)"
    )
    
    def soft_delete(self) -> None:
        """
        Realiza una eliminación lógica del registro
        """
        self.is_active = False
        self.deleted_at = func.now()
    
    def restore(self) -> None:
        """
        Restaura un registro eliminado lógicamente
        """
        self.is_active = True
        self.deleted_at = None
    
    @property
    def is_deleted(self) -> bool:
        """
        Verifica si el registro está eliminado lógicamente
        """
        return self.deleted_at is not None
