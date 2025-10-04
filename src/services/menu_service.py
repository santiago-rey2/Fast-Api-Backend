"""
Servicio para lógica de negocio del menú
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from src.repositories.menu_repository import MenuRepository

class MenuService:
    def __init__(self, db: Session):
        self.db = db
        self.menu_repo = MenuRepository(db)
    
    def get_platos_public(
        self, 
        categoria: Optional[str] = None,
        sugerencias: Optional[bool] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Lógica de negocio + transformación para API pública
        """
        # LÓGICA DE NEGOCIO: determinar qué platos mostrar
        is_active = self._determine_active_filter(sugerencias)
        
        # Usar repository (solo query)
        platos = self.menu_repo.get_platos_with_filters(
            categoria=categoria,
            sugerencias=sugerencias,
            precio_min=precio_min,
            precio_max=precio_max,
            is_active=is_active
        )
        
        # TRANSFORMACIÓN: agrupar y formatear para API
        return self._group_platos_by_category(platos)
    
    def _determine_active_filter(self, sugerencias: Optional[bool]) -> Optional[bool]:
        """
        REGLA DE NEGOCIO: cuándo mostrar platos activos/inactivos
        """
        if sugerencias is not None:
            # Si pide sugerencias, mostrar todos (activos e inactivos)
            # Si NO pide sugerencias, solo activos
            return None if sugerencias else True
        else:
            # Comportamiento por defecto: solo activos
            return True
    
    def _group_platos_by_category(self, platos: List) -> Dict[str, List[Dict[str, Any]]]:
        """
        TRANSFORMACIÓN: convertir objetos Plato a estructura para API
        """
        platos_agrupados = {}
        
        for plato in platos:
            categoria_nombre = plato.categoria.nombre
            
            # Crear la categoría si no existe
            if categoria_nombre not in platos_agrupados:
                platos_agrupados[categoria_nombre] = []
            
            # Transformar a diccionario para API
            plato_dict = {
                "id": plato.id,
                "nombre": plato.nombre,
                "descripcion": plato.descripcion,
                "precio": float(plato.precio) if plato.precio else None,
                "sugerencias": plato.sugerencias,
                "alergenos": [alergeno.nombre for alergeno in plato.alergenos] if plato.alergenos else []
            }
            
            platos_agrupados[categoria_nombre].append(plato_dict)
        
        return platos_agrupados