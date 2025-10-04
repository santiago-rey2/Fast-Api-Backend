"""
Servicio para lógica de negocio de los vinos
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from src.repositories.vinos_repository import VinosRepository

class VinosService:
    def __init__(self, db: Session):
        self.db = db
        self.vinos_repo = VinosRepository(db)
    
    def get_vinos_public(
        self,
        tipo: Optional[str] = None,
        denominacion: Optional[str] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None
    ) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Lógica de negocio + transformación para API pública
        """
        # Usar repository (devuelve objetos Vino)
        vinos = self.vinos_repo.get_vinos_with_filters(
            tipo=tipo,
            denominacion=denominacion,
            precio_min=precio_min,
            precio_max=precio_max,
            incluir_inactivos=False  # Solo activos para público
        )
        
        # TRANSFORMACIÓN: agrupar y formatear para API
        return self._group_vinos_by_type_and_denominacion(vinos)
    
    def _group_vinos_by_type_and_denominacion(self, vinos: List) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        TRANSFORMACIÓN: convertir objetos Vino a estructura para API
        """
        vinos_agrupados = {}
        
        for vino in vinos:
            tipo_vino = vino.categoria.nombre
            # Manejar denominación nula
            denominacion_nombre = vino.denominacion_origen.nombre if vino.denominacion_origen else "Sin denominación"
            
            # Crear el tipo si no existe
            if tipo_vino not in vinos_agrupados:
                vinos_agrupados[tipo_vino] = {}
            
            # Crear la denominación si no existe
            if denominacion_nombre not in vinos_agrupados[tipo_vino]:
                vinos_agrupados[tipo_vino][denominacion_nombre] = []
            
            # Obtener información adicional
            uvas_nombres = [uva.nombre for uva in vino.uvas] if vino.uvas else []
            enologo_nombre = vino.enologo.nombre if vino.enologo else None
            
            # Añadir el vino formateado
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