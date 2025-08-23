"""
Service para lógica de negocio de Vinos
"""
from typing import Optional, List, Tuple
from src.repositories.vinos import VinoRepository
from src.schemas.vino import VinoCreate, VinoUpdate
from src.entities.vino import Vino

class VinoService:
    def __init__(self, repo: VinoRepository) -> None:
        self.repo = repo

    def listar_vinos(
        self, 
        categoria_id: Optional[int] = None,
        bodega_id: Optional[int] = None,
        q: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        ordenar_por: str = "nombre"
    ) -> Tuple[List[Vino], int]:
        """Lista vinos con filtros y paginación"""
        vinos = self.repo.list(categoria_id, bodega_id, q, limit, offset, ordenar_por)
        total = self.repo.count(categoria_id, bodega_id, q)
        return list(vinos), total

    def obtener_vino(self, vino_id: int) -> Optional[Vino]:
        """Obtiene un vino por ID"""
        return self.repo.get_by_id(vino_id)

    def crear_vino(self, payload: VinoCreate) -> Vino:
        """Crea un nuevo vino"""
        return self.repo.create(
            nombre=payload.nombre,
            precio=payload.precio,
            categoria_id=payload.categoria_id,
            bodega_id=payload.bodega_id,
            denominacion_origen_id=payload.denominacion_origen_id,
            enologo_id=payload.enologo_id,
            uvas_ids=payload.uvas_ids
        )

    def actualizar_vino(self, vino_id: int, payload: VinoUpdate) -> Optional[Vino]:
        """Actualiza un vino existente"""
        return self.repo.update(
            vino_id=vino_id,
            nombre=payload.nombre,
            precio=payload.precio,
            categoria_id=payload.categoria_id,
            bodega_id=payload.bodega_id,
            denominacion_origen_id=payload.denominacion_origen_id,
            enologo_id=payload.enologo_id,
            uvas_ids=payload.uvas_ids
        )

    def eliminar_vino(self, vino_id: int) -> bool:
        """Elimina un vino"""
        return self.repo.delete(vino_id)
