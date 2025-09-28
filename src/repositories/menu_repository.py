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
    
    def get_platos_agrupados_por_categoria(
        self, 
        categoria: Optional[str] = None,
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
                "alergenos": alergenos_nombres
            }
            platos_agrupados[categoria_nombre].append(plato_dict)
        
        return platos_agrupados

    def get_vinos_agrupados_por_tipo_y_denominacion(
        self,
        tipo: Optional[str] = None,
        denominacion: Optional[str] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None
    ) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Obtiene todos los vinos agrupados por tipo y denominación con filtros opcionales
        """
        # Construir query base
        query = (
            self.db.query(Vino)
            .join(CategoriaVino)
            .join(DenominacionOrigen)
            .join(Bodega)
            .options(
                selectinload(Vino.uvas),
                selectinload(Vino.enologo)
            )
        )
        
        # Aplicar filtros
        filters = []
        
        if tipo:
            filters.append(CategoriaVino.nombre.ilike(f"%{tipo}%"))
        
        if denominacion:
            filters.append(DenominacionOrigen.nombre.ilike(f"%{denominacion}%"))
        
        if precio_min is not None:
            filters.append(Vino.precio >= precio_min)
        
        if precio_max is not None:
            filters.append(Vino.precio <= precio_max)
        
        if filters:
            query = query.filter(and_(*filters))
        
        vinos = query.order_by(CategoriaVino.nombre, DenominacionOrigen.nombre, Bodega.nombre).all()
        
        # Agrupar vinos por tipo -> denominación
        vinos_agrupados = {}
        for vino in vinos:
            tipo_vino = vino.categoria.nombre
            denominacion_nombre = vino.denominacion_origen.nombre
            
            # Crear el tipo si no existe
            if tipo_vino not in vinos_agrupados:
                vinos_agrupados[tipo_vino] = {}
            
            # Crear la denominación si no existe
            if denominacion_nombre not in vinos_agrupados[tipo_vino]:
                vinos_agrupados[tipo_vino][denominacion_nombre] = []
            
            # Obtener información adicional
            uvas_nombres = [uva.nombre for uva in vino.uvas] if vino.uvas else []
            enologo_nombre = vino.enologo.nombre if vino.enologo else None
            
            # Agregar vino a la estructura
            vino_dict = {
                "id": vino.id,
                "nombre": vino.nombre,
                "precio": float(vino.precio) if vino.precio else None,
                "bodega": vino.bodega.nombre,
                "uvas": uvas_nombres,
                "enologo": enologo_nombre
            }
            
            vinos_agrupados[tipo_vino][denominacion_nombre].append(vino_dict)
        
        return vinos_agrupados