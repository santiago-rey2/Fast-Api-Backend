"""
Service para lógica de negocio de Platos
"""
from typing import Optional, List, Tuple
from src.repositories.platos import PlatoRepository
from src.schemas.plato import PlatoCreate, PlatoUpdate
from src.entities.plato import Plato

class PlatoService:
    def __init__(self, repo: PlatoRepository) -> None:
        self.repo = repo

    def listar_platos(
        self, 
        categoria_id: Optional[int] = None,
        q: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        ordenar_por: str = "nombre"
    ) -> Tuple[List[Plato], int]:
        """Lista platos con paginación y filtros"""
        platos = self.repo.list(categoria_id, q, limit, offset, ordenar_por)
        total = self.repo.count(categoria_id, q)
        return list(platos), total

    def obtener_plato(self, plato_id: int) -> Optional[Plato]:
        """Obtiene un plato por ID"""
        return self.repo.get_by_id(plato_id)

    def crear_plato(self, payload: PlatoCreate) -> Plato:
        """Crea un nuevo plato"""
        return self.repo.create(
            nombre=payload.nombre,
            precio=payload.precio,
            descripcion=payload.descripcion,
            categoria_id=payload.categoria_id,
            alergenos_ids=payload.alergenos_ids
        )

    def actualizar_plato(self, plato_id: int, payload: PlatoUpdate) -> Optional[Plato]:
        """Actualiza un plato existente"""
        return self.repo.update(
            plato_id=plato_id,
            nombre=payload.nombre,
            precio=payload.precio,
            descripcion=payload.descripcion,
            categoria_id=payload.categoria_id,
            alergenos_ids=payload.alergenos_ids
        )

    def eliminar_plato(self, plato_id: int) -> bool:
        """Elimina un plato"""
        return self.repo.delete(plato_id)
