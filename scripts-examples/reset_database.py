#!/usr/bin/env python3
"""
Script para resetear completamente la base de datos y cargar datos por defecto.

Este script:
1. Elimina todas las tablas existentes
2. Recrea todas las tablas con campos de auditoría
3. Carga los datos por defecto (categorías, alérgenos, etc.)
4. Crea el usuario administrador por defecto

IMPORTANTE: Este script usa las entidades actualizadas con campos de auditoría
(created_at, updated_at, is_active, deleted_at)

Uso:
    python scripts-examples/reset_database.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text, inspect
from src.core.config import settings
from src.database import Base, init_db, _load_default_data
from src.auth.service import AuthService

def force_drop_all_tables():
    """Fuerza la eliminación de todas las tablas de la base de datos"""
    print("💥 Forzando eliminación de TODAS las tablas...")
    
    engine = create_engine(settings.sync_dsn, echo=False)
    
    with engine.connect() as conn:
        try:
            # Deshabilitar foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Obtener todas las tablas
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"   📋 Encontradas {len(tables)} tablas para eliminar")
                
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
                    print(f"   ⚠️  Aún quedan tablas: {remaining}")
                else:
                    print("   🎉 Todas las tablas eliminadas exitosamente")
            else:
                print("   ℹ️  No hay tablas para eliminar")
            
            # Rehabilitar foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            conn.commit()
            
        except Exception as e:
            print(f"❌ Error en force_drop_all_tables: {e}")
            return False
    
    return True

def reset_database():
    """Resetea completamente la base de datos"""
    print("�️  Iniciando reset de la base de datos...")
    
    engine = create_engine(settings.sync_dsn, echo=False)
    
    # Verificar conexión
    try:
        with engine.connect() as conn:
            print("✅ Conexión a la base de datos establecida")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Intentar eliminación estándar primero
    print("🗑️  Intentando eliminación estándar...")
    
    # Import all models to register them with Base.metadata
    from src.entities import (
        plato, vino, categoria_plato, categoria_vino,
        alergeno, bodega, denominacion_origen, enologo, uva, user
    )
    # Also import the mixins to ensure they're loaded
    from src.entities import mixins
    
    with engine.connect() as conn:
        try:
            # Deshabilitar foreign key checks
            print("� Deshabilitando foreign key checks...")
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Usar metadata para eliminar tablas en orden correcto
            Base.metadata.drop_all(bind=engine)
            print("✅ Eliminación por metadata exitosa")
            
            # Rehabilitar foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            conn.commit()
            
        except Exception as e:
            print(f"⚠️  Eliminación estándar falló: {e}")
            print("🔨 Intentando eliminación forzada...")
            
            # Si falla, usar eliminación forzada
            if not force_drop_all_tables():
                print("❌ No se pudieron eliminar las tablas")
                return False
    
    # Crear todas las tablas nuevamente
    print("🏗️  Creando tablas...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente")
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False
    
    # Cargar datos por defecto
    print("📦 Cargando datos por defecto...")
    try:
        _load_default_data()
        print("✅ Datos por defecto cargados")
    except Exception as e:
        print(f"❌ Error cargando datos por defecto: {e}")
        return False
    
    # Crear usuario administrador
    print("👤 Creando usuario administrador...")
    try:
        auth_service = AuthService()
        admin_user = auth_service.create_user(
            username="admin",
            password="admin123",
            role="admin"
        )
        print(f"✅ Usuario administrador creado: {admin_user.username}")
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        return False
    
    print("🎉 ¡Reset de base de datos completado exitosamente!")
    return True
        
        # 4. Cargar datos por defecto
        print("🌱 Cargando datos por defecto...")
        _load_default_data()
        print("✅ Datos por defecto cargados")
        
        print("\n🎉 ¡Base de datos reseteada exitosamente!")
        print("\n📋 Resumen de datos cargados:")
        print("   • 10 categorías de platos")
        print("   • 15 alérgenos (legislación española + sin alérgenos)")
        print("   • 11 categorías de vinos")
        print("   • 6 denominaciones de origen básicas")
        print("   • 11 tipos de uva comunes")
        print("\n🔍 Características de auditoría:")
        print("   • created_at: Fecha/hora de creación automática")
        print("   • updated_at: Fecha/hora de modificación automática")
        print("   • is_active: Control de estado (default: True)")
        print("   • deleted_at: Eliminación lógica (soft delete)")
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
    inspector = inspect(engine)
    
    try:
        with engine.connect() as conn:
            # Verificar datos básicos
            data_checks = [
                ("categoria_platos", "SELECT COUNT(*) FROM categoria_platos"),
                ("alergenos", "SELECT COUNT(*) FROM alergenos"),
                ("categoria_vinos", "SELECT COUNT(*) FROM categoria_vinos"),
                ("denominaciones_origen", "SELECT COUNT(*) FROM denominaciones_origen"),
                ("uvas", "SELECT COUNT(*) FROM uvas"),
                ("users", "SELECT COUNT(*) FROM users"),
            ]
            
            print("📊 Verificación de datos:")
            all_data_ok = True
            for table_name, query in data_checks:
                result = conn.execute(text(query))
                count = result.scalar()
                status = "✅" if count > 0 else "❌"
                print(f"   {status} {table_name}: {count} registros")
                if count == 0:
                    all_data_ok = False
            
            # Verificar campos de auditoría
            print("\n🔍 Verificación de campos de auditoría:")
            tables_to_check = [
                "platos", "vinos", "categoria_platos", "categoria_vinos", 
                "alergenos", "bodegas", "denominaciones_origen", "enologos", "uvas", "users"
            ]
            
            audit_fields = ['created_at', 'updated_at', 'is_active', 'deleted_at']
            all_audit_ok = True
            
            for table_name in tables_to_check:
                if inspector.has_table(table_name):
                    existing_columns = {col['name'] for col in inspector.get_columns(table_name)}
                    
                    missing_fields = []
                    for field in audit_fields:
                        if field not in existing_columns:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        print(f"   ❌ {table_name}: faltan campos {missing_fields}")
                        all_audit_ok = False
                    else:
                        print(f"   ✅ {table_name}: campos de auditoría completos")
                else:
                    print(f"   ⚠️  {table_name}: tabla no existe")
                    all_audit_ok = False
            
            if all_data_ok and all_audit_ok:
                print("\n✅ Verificación completada exitosamente")
                print("🎯 Base de datos lista con campos de auditoría")
            else:
                if not all_data_ok:
                    print("\n❌ Algunos datos no se cargaron correctamente")
                if not all_audit_ok:
                    print("❌ Algunos campos de auditoría faltan")
                
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")

if __name__ == "__main__":
    print("=" * 70)
    print("🔄 SCRIPT DE RESET DE BASE DE DATOS CON CAMPOS DE AUDITORÍA")
    print("=" * 70)
    print()
    print("Este script creará una base de datos completamente nueva con:")
    print("  🗂️  Estructura de tablas actualizada")
    print("  📅 Campos de auditoría (created_at, updated_at, is_active, deleted_at)")
    print("  🌱 Datos por defecto (categorías, alérgenos, etc.)")
    print("  👤 Usuario administrador (admin/admin123)")
    print()
    
    # Confirmar acción
    response = input("⚠️  ¿Estás seguro de que quieres ELIMINAR todos los datos? (y/N): ")
    
    if response.lower() != 'y':
        print("❌ Operación cancelada por el usuario")
        sys.exit(0)
    
    # Ejecutar reset
    success = reset_database()
    
    if success:
        # Verificar resultado
        verify_reset()
        print("\n🚀 La base de datos está lista para usar con campos de auditoría")
        print("💡 Puedes ejecutar 'python scripts-examples/load_sample_data.py' para cargar datos de ejemplo")
        print("🔍 Todos los registros tendrán campos de auditoría automáticos")
    else:
        print("\n💥 El reset falló. Revisa los errores anteriores.")
        sys.exit(1)
