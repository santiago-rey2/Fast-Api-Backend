#!/usr/bin/env python3
"""
Script para eliminar todas las tablas de la base de datos.

Este script elimina TODAS las tablas de la base de datos dejándola completamente vacía.
No carga ningún dato - solo eliminación.

Uso:
    python scripts-examples/clear_database.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from sqlalchemy import create_engine, text, inspect
    from src.core.config import settings
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Asegúrate de:")
    print("   1. Estar en el directorio raíz del proyecto")
    print("   2. Tener instaladas las dependencias: pip install -r requirements.txt")
    print("   3. Tener configurada la base de datos en src/core/config.py")
    sys.exit(1)

def force_drop_all_tables():
    """Fuerza la eliminación de todas las tablas de la base de datos"""
    print("💥 Eliminando TODAS las tablas de la base de datos...")
    
    engine = create_engine(settings.sync_dsn, echo=False)
    
    with engine.connect() as conn:
        try:
            # Deshabilitar foreign key checks
            print("🔓 Deshabilitando foreign key checks...")
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Obtener todas las tablas
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"📋 Encontradas {len(tables)} tablas para eliminar: {tables}")
                
                # Eliminar cada tabla
                for table in tables:
                    try:
                        conn.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
                        print(f"   ✅ Eliminada: {table}")
                    except Exception as e:
                        print(f"   ❌ Error con {table}: {e}")
                
                # Verificar que no queden tablas
                result = conn.execute(text("SHOW TABLES"))
                remaining = [row[0] for row in result.fetchall()]
                
                if remaining:
                    print(f"⚠️  Aún quedan tablas: {remaining}")
                    return False
                else:
                    print("🎉 Todas las tablas eliminadas exitosamente")
            else:
                print("ℹ️  No hay tablas para eliminar - la base de datos ya está vacía")
            
            # Rehabilitar foreign key checks
            print("🔒 Rehabilitando foreign key checks...")
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            conn.commit()
            
        except Exception as e:
            print(f"❌ Error eliminando tablas: {e}")
            return False
    
    return True

def reset_database():
    """Elimina todas las tablas de la base de datos dejándola completamente vacía"""
    print("🗂️  Iniciando eliminación completa de tablas...")
    
    engine = create_engine(settings.sync_dsn, echo=False)
    
    # Verificar conexión
    try:
        with engine.connect() as conn:
            print("✅ Conexión a la base de datos establecida")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Eliminar todas las tablas
    print("🗑️  Eliminando todas las tablas...")
    
    if force_drop_all_tables():
        print("🎉 ¡Base de datos vaciada exitosamente!")
        print("📝 La base de datos está ahora completamente vacía")
        return True
    else:
        print("❌ No se pudieron eliminar todas las tablas")
        return False

def verify_empty_database():
    """Verifica que la base de datos esté completamente vacía"""
    print("\n🔍 Verificando que la base de datos esté vacía...")
    
    engine = create_engine(settings.sync_dsn, echo=False)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"❌ La base de datos NO está vacía. Tablas restantes: {tables}")
                return False
            else:
                print("✅ Verificación exitosa: la base de datos está completamente vacía")
                return True
                
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🗑️  SCRIPT DE VACIADO COMPLETO DE BASE DE DATOS")
    print("=" * 60)
    print()
    print("⚠️  Este script eliminará TODAS las tablas de la base de datos")
    print("🔄 La base de datos quedará completamente vacía")
    print("📝 NO se cargarán datos - solo eliminación")
    print()
    
    # Confirmar acción
    response = input("¿Estás seguro de que quieres ELIMINAR todas las tablas? (y/N): ")
    
    if response.lower() != 'y':
        print("❌ Operación cancelada por el usuario")
        sys.exit(0)
    
    # Ejecutar eliminación
    success = reset_database()
    
    if success:
        # Verificar resultado
        if verify_empty_database():
            print("\n🚀 Operación completada exitosamente")
            print("💡 La base de datos está lista para crear nuevas tablas")
        else:
            print("\n⚠️  La operación se completó pero quedan algunas tablas")
    else:
        print("\n💥 La eliminación falló. Revisa los errores anteriores.")
        sys.exit(1)
