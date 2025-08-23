"""
Script de prueba para verificar las importaciones
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔍 Probando importaciones...")
    
    # Probar importación de la base de datos
    from src.database import get_db, SessionLocal
    print("✅ Database imports: OK")
    
    # Probar importación de entidades
    from src.entities.categoria_plato import CategoriaPlato
    from src.entities.alergeno import Alergeno
    from src.entities.categoria_vino import CategoriaVino
    from src.entities.bodega import Bodega
    print("✅ Entity imports: OK")
    
    # Probar importación de schemas
    from src.schemas.admin import CategoriaCreate, AlerganoCreate
    print("✅ Schema imports: OK")
    
    # Probar importación de rutas
    from src.routes.admin import router as admin_router
    print("✅ Admin routes import: OK")
    
    # Probar importación principal
    from src.main import app
    print("✅ Main app import: OK")
    
    print("\n🎉 ¡Todas las importaciones funcionan correctamente!")
    print("✅ El servidor debería iniciarse sin problemas")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    import traceback
    traceback.print_exc()
