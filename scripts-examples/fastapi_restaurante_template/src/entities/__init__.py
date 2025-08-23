# Import all entities to register them with SQLAlchemy
from .categoria_plato import CategoriaPlato
from .alergeno import Alergeno
from .plato import Plato
from .categoria_vino import CategoriaVino
from .bodega import Bodega
from .denominacion_origen import DenominacionOrigen
from .enologo import Enologo
from .uva import Uva
from .vino import Vino

__all__ = [
    "CategoriaPlato",
    "Alergeno", 
    "Plato",
    "CategoriaVino",
    "Bodega",
    "DenominacionOrigen",
    "Enologo",
    "Uva",
    "Vino"
]
