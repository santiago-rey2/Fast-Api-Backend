#!/usr/bin/env python3
"""
Script para resetear completamente la base de datos y cargar datos por defecto.

Este script:
1. Elimina todas las tablas existentes
2. Recrea todas las tablas
3. Carga los datos por defecto (categorías, alérgenos, etc.)
4. Crea el usuario administrador por defecto

Uso:
    python scripts-examples/reset_database.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from src.core.config import settings
from src.database import Base, init_db, _load_default_data
from src.auth.service import AuthService

def reset_database():
    """Resetea completamente la base de datos"""
    print("🔥 Iniciando reset de la base de datos...")
    
    # Crear conexión a la base de datos
    engine = create_engine(settings.sync_dsn, echo=False)
    
    try:
        # 1. Eliminar todas las tablas
        print("🗑️  Eliminando todas las tablas...")
        
        # Import all models to register them with Base.metadata
        from src.entities import (
            plato, vino, categoria_plato, categoria_vino,
            alergeno, bodega, denominacion_origen, enologo, uva, user
        )
        
        # Eliminar todas las tablas
        Base.metadata.drop_all(bind=engine)
        print("✅ Todas las tablas eliminadas correctamente")
        
        # 2. Recrear todas las tablas
        print("🏗️  Recreando estructura de tablas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Estructura de tablas recreada")
        
        # 3. Cargar datos por defecto
        print("🌱 Cargando datos por defecto...")
        _load_default_data()
        print("✅ Datos por defecto cargados")
        
        print("\n🎉 ¡Base de datos reseteada exitosamente!")
        print("\n📋 Resumen de datos cargados:")
        print("   • 10 categorías de platos")
        print("   • 14 alérgenos (legislación española)")
        print("   • 10 categorías de vinos")
        print("   • 5 denominaciones de origen básicas")
        print("   • 10 tipos de uva comunes")
        print("\n👤 Usuario administrador:")
        print("   • Username: admin")
        print("   • Password: admin123")
        print("   • Email: admin@restaurant.com")
        
    except Exception as e:
        print(f"❌ Error durante el reset: {e}")
        return False
    
    return True

def verify_reset():
    """Verifica que el reset se haya completado correctamente"""
    print("\n🔍 Verificando reset...")
    
    engine = create_engine(settings.sync_dsn, echo=False)
    
    try:
        with engine.connect() as conn:
            # Verificar datos básicos
            checks = [
                ("categoria_platos", "SELECT COUNT(*) FROM categoria_platos"),
                ("alergenos", "SELECT COUNT(*) FROM alergenos"),
                ("categoria_vinos", "SELECT COUNT(*) FROM categoria_vinos"),
                ("users", "SELECT COUNT(*) FROM users"),
            ]
            
            all_ok = True
            for table_name, query in checks:
                result = conn.execute(text(query))
                count = result.scalar()
                status = "✅" if count > 0 else "❌"
                print(f"   {status} {table_name}: {count} registros")
                if count == 0:
                    all_ok = False
            
            if all_ok:
                print("\n✅ Verificación completada exitosamente")
            else:
                print("\n❌ Algunos datos no se cargaron correctamente")
                
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 SCRIPT DE RESET DE BASE DE DATOS")
    print("=" * 60)
    
    # Confirmar acción
    response = input("\n⚠️  ¿Estás seguro de que quieres ELIMINAR todos los datos? (y/N): ")
    
    if response.lower() != 'y':
        print("❌ Operación cancelada por el usuario")
        sys.exit(0)
    
    # Ejecutar reset
    success = reset_database()
    
    if success:
        # Verificar resultado
        verify_reset()
        print("\n🚀 La base de datos está lista para usar")
        print("💡 Puedes ejecutar 'python scripts-examples/load_sample_data.py' para cargar datos de ejemplo")
    else:
        print("\n💥 El reset falló. Revisa los errores anteriores.")
        sys.exit(1)
