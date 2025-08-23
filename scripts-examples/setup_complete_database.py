#!/usr/bin/env python3
"""
Script completo para resetear la base de datos y cargar datos de ejemplo.

Este script ejecuta en secuencia:
1. Reset completo de la base de datos
2. Carga de datos por defecto
3. Carga de datos de ejemplo

Uso:
    python scripts-examples/setup_complete_database.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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
    print("  4. 🎭 Cargar datos de ejemplo (platos y vinos realistas)")
    print()
    
    # Confirmar acción
    response = input("⚠️  ¿Continuar? (y/N): ")
    
    if response.lower() != 'y':
        print("❌ Operación cancelada por el usuario")
        sys.exit(0)
    
    try:
        # Importar y ejecutar reset
        print("\n" + "="*50)
        print("PASO 1: RESET DE BASE DE DATOS")
        print("="*50)
        
        # Importar módulos necesarios
        import importlib.util
        import sys
        
        # Cargar el módulo reset_database
        spec = importlib.util.spec_from_file_location("reset_database", 
                                                     project_root / "scripts-examples" / "reset_database.py")
        reset_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reset_module)
        
        success = reset_module.reset_database()
        if not success:
            print("❌ Error en el reset. Abortando.")
            sys.exit(1)
        
        reset_module.verify_reset()
        
        # Importar y ejecutar carga de datos de ejemplo
        print("\n" + "="*50)
        print("PASO 2: CARGA DE DATOS DE EJEMPLO")
        print("="*50)
        
        # Cargar el módulo load_sample_data
        spec = importlib.util.spec_from_file_location("load_sample_data", 
                                                     project_root / "scripts-examples" / "load_sample_data.py")
        sample_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sample_module)
        
        db = sample_module.create_session()
        
        try:
            sample_module.load_sample_bodegas(db)
            sample_module.load_sample_enologos(db)
            sample_module.load_sample_platos(db)
            sample_module.load_sample_vinos(db)
            
            sample_module.verify_sample_data(db)
            
        finally:
            db.close()
        
        # Resumen final
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
        print("   • Email: admin@restaurant.com")
        print()
        print("🚀 Para iniciar el servidor:")
        print("   python -m uvicorn src.main:app --reload")
        print()
        print("📖 Documentación de la API:")
        print("   http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Error durante el setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
