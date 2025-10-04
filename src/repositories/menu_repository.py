"""
Repository para manejar queries de menú
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_
from src.entities.plato import Plato
from src.entities.categoria_plato import CategoriaPlato
from src.entities.vino import Vino
from src.entities.categoria_vino import CategoriaVino
from src.entities.denominacion_origen import DenominacionOrigen
from src.entities.bodega import Bodega

class MenuRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_platos_public(
        self, 
        categoria: Optional[str] = None,
        sugerencias: Optional[bool] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Obtiene todos los platos agrupados por categoría con filtros opcionales
        """
        # Construir query base
        query = (
            self.db.query(Plato)
            .join(CategoriaPlato)
            .options(selectinload(Plato.alergenos))
        )
        
        # Aplicar filtros
        filters = []
        
        if categoria:
            filters.append(CategoriaPlato.nombre.ilike(f"%{categoria}%"))
        
        if precio_min is not None:
            filters.append(Plato.precio >= precio_min)
        
        if precio_max is not None:
            filters.append(Plato.precio <= precio_max)

        if sugerencias is not None:
            filters.append(Plato.sugerencias == sugerencias)
            # Si NO se están pidiendo sugerencias (sugerencias=False o None para carta normal),
            # solo mostrar platos activos
            if not sugerencias:
                filters.append(Plato.is_active == True)
        else:
            # Si no se especifica el parámetro sugerencias, mostrar solo platos activos
            # (comportamiento por defecto para la carta)
            filters.append(Plato.is_active == True)
        
        if filters:
            query = query.filter(and_(*filters))
        
        platos = query.all()
        
        # Agrupar platos por categoría
        platos_agrupados = {}
        for plato in platos:
            categoria_nombre = plato.categoria.nombre
            
            # Crear la categoría si no existe
            if categoria_nombre not in platos_agrupados:
                platos_agrupados[categoria_nombre] = []
            
            # Obtener lista de alérgenos
            alergenos_nombres = [alergeno.nombre for alergeno in plato.alergenos] if plato.alergenos else []
            
            # Agregar plato a la categoría con alérgenos
            plato_dict = {
                "id": plato.id,
                "nombre": plato.nombre,
                "descripcion": plato.descripcion,
                "precio": float(plato.precio) if plato.precio else None,
                "sugerencias": plato.sugerencias,
                "alergenos": alergenos_nombres
            }
            platos_agrupados[categoria_nombre].append(plato_dict)
        
        return platos_agrupados