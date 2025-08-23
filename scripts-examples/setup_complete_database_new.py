#!/usr/bin/env python3
"""
Script completo para resetear la base de datos y cargar datos de ejemplo.

Este script ejecuta en secuencia:
1. Elimina todas las tablas existentes
2. Recrea la estructura de la base de datos
3. Carga datos por defecto (categorías, alérgenos, etc.)
4. Crea usuario administrador
5. Carga datos de ejemplo (platos y vinos)

Uso:
    python scripts-examples/setup_complete_database.py
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
    from src.database import Base, init_db, _load_default_data
    from src.auth.service import AuthService
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Asegúrate de:")
    print("   1. Estar en el directorio raíz del proyecto")
    print("   2. Tener instaladas las dependencias: pip install -r requirements.txt")
    print("   3. Tener configurada la base de datos en src/core/config.py")
    sys.exit(1)

def clear_all_tables():
    """Elimina todas las tablas de la base de datos"""
    print("🗑️  Eliminando todas las tablas...")
    
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
                        return False
                
                # Verificar que no queden tablas
                result = conn.execute(text("SHOW TABLES"))
                remaining = [row[0] for row in result.fetchall()]
                
                if remaining:
                    print(f"   ⚠️  Aún quedan tablas: {remaining}")
                    return False
                else:
                    print("   🎉 Todas las tablas eliminadas exitosamente")
            else:
                print("   ℹ️  No hay tablas para eliminar")
            
            # Rehabilitar foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            conn.commit()
            
            return True
            
        except Exception as e:
            print(f"❌ Error eliminando tablas: {e}")
            return False

def create_database_structure():
    """Crea la estructura de la base de datos"""
    print("🏗️  Creando estructura de la base de datos...")
    
    try:
        # Import all models to register them with Base.metadata
        from src.entities import (
            plato, vino, categoria_plato, categoria_vino,
            alergeno, bodega, denominacion_origen, enologo, uva, user
        )
        # Also import the mixins to ensure they're loaded
        from src.entities import mixins
        
        engine = create_engine(settings.sync_dsn, echo=False)
        Base.metadata.create_all(bind=engine)
        print("✅ Estructura de tablas creada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando estructura: {e}")
        return False

def load_default_data():
    """Carga datos por defecto"""
    print("📦 Cargando datos por defecto...")
    
    try:
        _load_default_data()
        print("✅ Datos por defecto cargados")
        return True
        
    except Exception as e:
        print(f"❌ Error cargando datos por defecto: {e}")
        return False

def create_admin_user():
    """Crea usuario administrador"""
    print("👤 Creando usuario administrador...")
    
    try:
        auth_service = AuthService()
        admin_user = auth_service.create_user(
            username="admin",
            password="admin123",
            role="admin"
        )
        print(f"✅ Usuario administrador creado: {admin_user.username}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        return False

def load_sample_data():
    """Carga datos de ejemplo usando el script existente"""
    print("🎭 Cargando datos de ejemplo...")
    
    try:
        # Importar el módulo de carga de datos de ejemplo
        import importlib.util
        
        # Cargar el módulo load_sample_data
        spec = importlib.util.spec_from_file_location("load_sample_data", 
                                                     project_root / "scripts-examples" / "load_sample_data.py")
        sample_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sample_module)
        
        # Ejecutar la función main del módulo
        sample_module.main()
        return True
        
    except Exception as e:
        print(f"❌ Error cargando datos de ejemplo: {e}")
        return False

def verify_setup():
    """Verifica que el setup se haya completado correctamente"""
    print("\n🔍 Verificando setup completo...")
    
    engine = create_engine(settings.sync_dsn, echo=False)
    
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
                ("platos", "SELECT COUNT(*) FROM platos"),
                ("vinos", "SELECT COUNT(*) FROM vinos"),
                ("bodegas", "SELECT COUNT(*) FROM bodegas"),
                ("enologos", "SELECT COUNT(*) FROM enologos"),
            ]
            
            print("📊 Verificación de datos:")
            all_ok = True
            for table_name, query in data_checks:
                try:
                    result = conn.execute(text(query))
                    count = result.scalar()
                    status = "✅" if count > 0 else "❌"
                    print(f"   {status} {table_name}: {count} registros")
                    if count == 0 and table_name in ["categoria_platos", "alergenos", "users"]:
                        all_ok = False
                except Exception as e:
                    print(f"   ❌ Error verificando {table_name}: {e}")
                    all_ok = False
            
            return all_ok
                
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

def main():
    """Función principal que ejecuta el setup completo"""
    print("=" * 70)
    print("🚀 SETUP COMPLETO DE BASE DE DATOS")
    print("=" * 70)
    print()
    print("Este script va a:")
    print("  1. 🔥 ELIMINAR todos los datos existentes")
    print("  2. 🏗️  Recrear la estructura de la base de datos")
    print("  3. 🌱 Cargar datos por defecto (categorías, alérgenos, etc.)")
    print("  4. 👤 Crear usuario administrador (admin/admin123)")
    print("  5. 🎭 Cargar datos de ejemplo (platos y vinos realistas)")
    print()
    
    # Confirmar acción
    response = input("⚠️  ¿Continuar? (y/N): ")
    
    if response.lower() != 'y':
        print("❌ Operación cancelada por el usuario")
        sys.exit(0)
    
    print()
    
    # Ejecutar pasos del setup
    steps = [
        ("Eliminar tablas existentes", clear_all_tables),
        ("Crear estructura de BD", create_database_structure),
        ("Cargar datos por defecto", load_default_data),
        ("Crear usuario administrador", create_admin_user),
        ("Cargar datos de ejemplo", load_sample_data),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*50}")
        print(f"PASO: {step_name.upper()}")
        print("="*50)
        
        if not step_func():
            print(f"\n❌ Error en: {step_name}")
            print("💥 Setup abortado")
            sys.exit(1)
    
    # Verificar resultado
    if verify_setup():
        print("\n" + "="*70)
        print("🎉 ¡SETUP COMPLETO EXITOSO!")
        print("="*70)
        print()
        print("📊 Base de datos configurada con:")
        print("   • ✅ Datos por defecto (categorías, alérgenos, etc.)")
        print("   • ✅ Datos de ejemplo (platos y vinos realistas)")
        print("   • ✅ Usuario administrador creado")
        print()
        print("🔐 Credenciales de administrador:")
        print("   • Username: admin")
        print("   • Password: admin123")
        print("   • Role: admin")
        print()
        print("🚀 Para iniciar el servidor:")
        print("   python -m uvicorn src.main:app --reload")
        print()
        print("📖 Documentación de la API:")
        print("   http://localhost:8000/docs")
        print()
        print("🎯 Endpoints públicos (sin autenticación):")
        print("   GET /api/v1/platos/ - Lista de platos")
        print("   GET /api/v1/vinos/ - Lista de vinos")
        print()
        print("🔒 Endpoints protegidos (requieren autenticación admin):")
        print("   POST/PUT/DELETE en todos los recursos")
    else:
        print("\n⚠️  Setup completado pero con algunos problemas en la verificación")
        print("💡 Revisa los mensajes anteriores para más detalles")

if __name__ == "__main__":
    main()
