#!/usr/bin/env python3
"""
Script para configurar una base de datos completa con todos los datos por defecto
necesarios para el funcionamiento del sistema de restaurante.

Este script inicializa:
- Tablas de la base de datos
- Datos por defecto (categorías, alérgenos, etc.)
- Datos de configuración inicial

Uso:
    python scripts-examples/setup_complete_database.py
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from src.core.config import settings
    from src.database import Base, init_db
    from src.auth.service import AuthService
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Asegúrate de:")
    print("   1. Estar en el directorio raíz del proyecto")
    print("   2. Tener instaladas las dependencias: pip install -r requirements.txt")
    print("   3. Tener configurada la base de datos en src/core/config.py")
    sys.exit(1)

def setup_database():
    """Configura la base de datos completa"""
    print("🚀 Iniciando configuración completa de la base de datos...")
    
    try:
        engine = create_engine(settings.sync_dsn, echo=False)
        SessionLocal = sessionmaker(bind=engine)
        
        # Crear todas las tablas
        print("📋 Creando estructura de tablas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas")
        
        # Cargar datos por defecto expandidos
        load_extended_default_data(engine)
        
        print("🎉 ¡Base de datos configurada exitosamente!")
        print("💡 Ahora puedes ejecutar:")
        print("   - python scripts-examples/load_sample_data.py (para datos de ejemplo)")
        print("   - uvicorn src.main:app --reload (para iniciar el servidor)")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        raise

def load_extended_default_data(engine):
    """Carga datos por defecto expandidos"""
    with engine.connect() as conn:
        # Configurar modo SQL para permitir ID 0
        conn.execute(text("SET SESSION sql_mode = 'NO_AUTO_VALUE_ON_ZERO'"))
        
        # Verificar si ya existen datos (para evitar duplicados)
        result = conn.execute(text("SELECT COUNT(*) FROM categoria_platos"))
        if result.scalar() > 0:
            print("ℹ️  Los datos por defecto ya están cargados")
            return
        
        print("🌱 Cargando datos por defecto expandidos...")
        
        # === USUARIO ADMINISTRADOR ===
        print("👤 Creando usuario administrador...")
        hashed_password = AuthService.get_password_hash("admin123")
        conn.execute(text("""
            INSERT IGNORE INTO users (username, email, hashed_password, is_active, is_admin) VALUES
            ('admin', 'admin@restaurant.com', :password, true, true)
        """), {"password": hashed_password})
        
        # === CATEGORÍAS DE PLATOS EXPANDIDAS ===
        print("📂 Cargando categorías de platos...")
        conn.execute(text("""
            INSERT IGNORE INTO categoria_platos (id, nombre) VALUES
            (0, 'Sin categoría'),
            (1, 'Entrantes'),
            (2, 'Principales'), 
            (3, 'Postres'),
            (4, 'Ensaladas'),
            (5, 'Tapas'),
            (6, 'Arroces'),
            (7, 'Carnes'),
            (8, 'Pescados'),
            (9, 'Mariscos'),
            (10, 'Sopas'),
            (11, 'Verduras'),
            (12, 'Pasta'),
            (13, 'Quesos'),
            (14, 'Aperitivos')
        """))
        
        # === ALÉRGENOS SEGÚN LEY ESPAÑOLA ===
        print("🚨 Cargando alérgenos oficiales...")
        conn.execute(text("""
            INSERT IGNORE INTO alergenos (id, nombre) VALUES
            (0, 'Sin alérgenos'),
            (1, 'Gluten'),
            (2, 'Crustáceos'),
            (3, 'Huevos'),
            (4, 'Pescado'),
            (5, 'Cacahuetes'),
            (6, 'Soja'),
            (7, 'Lácteos'),
            (8, 'Frutos secos'),
            (9, 'Apio'),
            (10, 'Mostaza'),
            (11, 'Sésamo'),
            (12, 'Sulfitos'),
            (13, 'Altramuces'),
            (14, 'Moluscos')
        """))
        
        # === CATEGORÍAS DE VINOS EXPANDIDAS ===
        print("🍷 Cargando categorías de vinos...")
        conn.execute(text("""
            INSERT IGNORE INTO categoria_vinos (id, nombre) VALUES
            (0, 'Sin categoría'),
            (1, 'Tinto joven'),
            (2, 'Tinto crianza'),
            (3, 'Tinto reserva'),
            (4, 'Tinto gran reserva'),
            (5, 'Blanco joven'),
            (6, 'Blanco crianza'),
            (7, 'Blanco reserva'),
            (8, 'Rosado'),
            (9, 'Espumoso'),
            (10, 'Dulce'),
            (11, 'Generoso'),
            (12, 'Licoroso'),
            (13, 'Fortificado')
        """))
        
        # === DENOMINACIONES DE ORIGEN ESPAÑOLAS ===
        print("🏷️ Cargando denominaciones de origen...")
        conn.execute(text("""
            INSERT IGNORE INTO denominaciones_origen (id, nombre, region) VALUES
            (0, 'Sin D.O.', 'Sin especificar'),
            
            -- Castilla y León
            (1, 'D.O. Ribera del Duero', 'Castilla y León'),
            (2, 'D.O. Rueda', 'Castilla y León'),
            (3, 'D.O. Toro', 'Castilla y León'),
            (4, 'D.O. Cigales', 'Castilla y León'),
            (5, 'D.O. Bierzo', 'Castilla y León'),
            
            -- La Rioja
            (6, 'D.O. Rioja', 'La Rioja'),
            
            -- Cataluña
            (7, 'D.O. Penedès', 'Cataluña'),
            (8, 'D.O. Priorat', 'Cataluña'),
            (9, 'D.O. Montsant', 'Cataluña'),
            (10, 'D.O. Cava', 'Cataluña'),
            
            -- Galicia
            (11, 'D.O. Rías Baixas', 'Galicia'),
            (12, 'D.O. Ribeiro', 'Galicia'),
            (13, 'D.O. Valdeorras', 'Galicia'),
            
            -- Andalucía
            (14, 'D.O. Jerez', 'Andalucía'),
            (15, 'D.O. Montilla-Moriles', 'Andalucía'),
            (16, 'D.O. Málaga', 'Andalucía'),
            
            -- Valencia
            (17, 'D.O. Valencia', 'Valencia'),
            (18, 'D.O. Utiel-Requena', 'Valencia'),
            (19, 'D.O. Alicante', 'Valencia'),
            
            -- Aragón
            (20, 'D.O. Somontano', 'Aragón'),
            (21, 'D.O. Campo de Borja', 'Aragón'),
            (22, 'D.O. Cariñena', 'Aragón'),
            
            -- Navarra
            (23, 'D.O. Navarra', 'Navarra'),
            
            -- País Vasco
            (24, 'D.O. Txakoli de Getaria', 'País Vasco'),
            
            -- Murcia
            (25, 'D.O. Jumilla', 'Murcia'),
            (26, 'D.O. Yecla', 'Murcia'),
            
            -- Castilla-La Mancha
            (27, 'D.O. Valdepeñas', 'Castilla-La Mancha'),
            (28, 'D.O. La Mancha', 'Castilla-La Mancha'),
            
            -- Extremadura
            (29, 'D.O. Ribera del Guadiana', 'Extremadura'),
            
            -- Canarias
            (30, 'D.O. Tacoronte-Acentejo', 'Canarias'),
            
            -- Otros
            (31, 'V.T. Castilla', 'Vino de la Tierra'),
            (32, 'V.T. Castilla y León', 'Vino de la Tierra')
        """))
        
        # === VARIEDADES DE UVA ESPAÑOLAS ===
        print("🍇 Cargando variedades de uva...")
        conn.execute(text("""
            INSERT IGNORE INTO uvas (id, nombre, tipo) VALUES
            (0, 'Sin uva', 'Sin tipo'),
            
            -- Uvas tintas españolas
            (1, 'Tempranillo', 'Tinta'),
            (2, 'Garnacha', 'Tinta'),
            (3, 'Monastrell', 'Tinta'),
            (4, 'Bobal', 'Tinta'),
            (5, 'Mencía', 'Tinta'),
            (6, 'Graciano', 'Tinta'),
            (7, 'Mazuelo', 'Tinta'),
            (8, 'Cariñena', 'Tinta'),
            (9, 'Tinta de Toro', 'Tinta'),
            (10, 'Prieto Picudo', 'Tinta'),
            
            -- Uvas tintas internacionales
            (11, 'Cabernet Sauvignon', 'Tinta'),
            (12, 'Merlot', 'Tinta'),
            (13, 'Syrah', 'Tinta'),
            (14, 'Pinot Noir', 'Tinta'),
            (15, 'Cabernet Franc', 'Tinta'),
            
            -- Uvas blancas españolas
            (16, 'Albariño', 'Blanca'),
            (17, 'Verdejo', 'Blanca'),
            (18, 'Godello', 'Blanca'),
            (19, 'Viura', 'Blanca'),
            (20, 'Palomino', 'Blanca'),
            (21, 'Pedro Ximénez', 'Blanca'),
            (22, 'Airén', 'Blanca'),
            (23, 'Macabeo', 'Blanca'),
            (24, 'Xarel·lo', 'Blanca'),
            (25, 'Parellada', 'Blanca'),
            (26, 'Moscatel', 'Blanca'),
            (27, 'Malvasía', 'Blanca'),
            (28, 'Treixadura', 'Blanca'),
            (29, 'Loureiro', 'Blanca'),
            (30, 'Caiño', 'Blanca'),
            
            -- Uvas blancas internacionales
            (31, 'Chardonnay', 'Blanca'),
            (32, 'Sauvignon Blanc', 'Blanca'),
            (33, 'Riesling', 'Blanca'),
            (34, 'Gewürztraminer', 'Blanca'),
            (35, 'Pinot Grigio', 'Blanca')
        """))
        
        # === BODEGAS BASE PARA EMPEZAR ===
        print("🏭 Cargando bodegas base...")
        conn.execute(text("""
            INSERT IGNORE INTO bodegas (id, nombre, region) VALUES
            (0, 'Sin bodega', 'Sin región'),
            (1, 'Marqués de Riscal', 'Rioja'),
            (2, 'Vega Sicilia', 'Ribera del Duero'),
            (3, 'Torres', 'Penedès'),
            (4, 'Martín Códax', 'Rías Baixas'),
            (5, 'González Byass', 'Jerez')
        """))
        
        # === ENÓLOGOS BASE ===
        print("👨‍🔬 Cargando enólogos base...")
        conn.execute(text("""
            INSERT IGNORE INTO enologos (id, nombre) VALUES
            (0, 'Sin enólogo'),
            (1, 'Francisco Hurtado de Amézaga'),
            (2, 'Miguel Torres Maczassek'),
            (3, 'Pablo Álvarez'),
            (4, 'Mariano García'),
            (5, 'Telmo Rodríguez')
        """))
        
        conn.commit()
        
        print("✅ Datos por defecto expandidos cargados correctamente")
        print("📊 Resumen de datos cargados:")
        print("   - 15 categorías de platos")
        print("   - 15 alérgenos oficiales")
        print("   - 14 categorías de vinos")
        print("   - 33 denominaciones de origen")
        print("   - 36 variedades de uva")
        print("   - 6 bodegas base")
        print("   - 6 enólogos base")
        print("")
        print("👤 Usuario administrador creado:")
        print("   - Username: admin")
        print("   - Password: admin123")
        print("   - Email: admin@restaurant.com")

def main():
    """Función principal"""
    print("🔧 Configurador de Base de Datos del Restaurante")
    print("=" * 50)
    
    response = input("¿Continuar con la configuración de la base de datos? (y/N): ")
    if response.lower() != 'y':
        print("Operación cancelada")
        return
    
    setup_database()
    
    print("")
    print("🎯 Próximos pasos recomendados:")
    print("1. Ejecutar: python scripts-examples/load_sample_data.py")
    print("2. Iniciar servidor: uvicorn src.main:app --reload")
    print("3. Visitar documentación: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
