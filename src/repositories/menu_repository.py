"""
Repository para manejar queries de menú
"""
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from src.entities.plato import Plato
from src.entities.categoria_plato import CategoriaPlato

class MenuRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_platos_agrupados_por_categoria(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Obtiene todos los platos agrupados por categoría
        """
        # Query para obtener platos con sus categorías
        platos = self.db.query(Plato).join(CategoriaPlato).all()
        
        # Agrupar platos por categoría
        platos_agrupados = {}
        for plato in platos:
            categoria_nombre = plato.categoria.nombre
            
            # Crear la categoría si no existe
            if categoria_nombre not in platos_agrupados:
                platos_agrupados[categoria_nombre] = []
            
            # Agregar plato a la categoría
            plato_dict = {
                "id": plato.id,
                "nombre": plato.nombre,
                "descripcion": plato.descripcion,
                "precio": float(plato.precio) if plato.precio else None
            }
            platos_agrupados[categoria_nombre].append(plato_dict)
        
        return platos_agrupados