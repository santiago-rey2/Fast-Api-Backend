#!/usr/bin/env python3
"""
Script para eliminar todas las tablas de la base de datos
Las tablas se recrearán automáticamente al levantar el servidor FastAPI
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import text
from src.database import engine

def drop_all_tables():
    """
    Elimina todas las tablas de la base de datos
    """
    print("�️  ELIMINANDO TODAS LAS TABLAS DE LA BASE DE DATOS...")
    
    with engine.connect() as conn:
        # Deshabilitar foreign key checks para poder eliminar tablas
        print("🔓 Deshabilitando foreign key checks...")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        # Obtener todas las tablas de la base de datos
        print("📋 Obteniendo lista de tablas...")
        result = conn.execute(text("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = DATABASE()
        """))
        tables = [row[0] for row in result.fetchall()]
        
        if not tables:
            print("ℹ️  No hay tablas para eliminar")
        else:
            # Eliminar todas las tablas una por una
            print(f"🗑️  Eliminando {len(tables)} tablas...")
            for table in tables:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
                    print(f"   ✅ Eliminada: {table}")
                except Exception as e:
                    print(f"   ⚠️  Error eliminando {table}: {e}")
        
        # Rehabilitar foreign key checks
        print("🔒 Rehabilitando foreign key checks...")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        
        conn.commit()
    
    print("\n✅ Todas las tablas han sido eliminadas")
    print("🚀 Las tablas se recrearán automáticamente cuando levantes el servidor FastAPI")
    print("💡 Ejecuta: fastapi dev src/main.py")

if __name__ == "__main__":
    try:
        drop_all_tables()
        print("\n🎉 ¡Eliminación completada exitosamente!")
    except Exception as e:
        print(f"\n❌ Error durante la eliminación: {e}")
        sys.exit(1)
