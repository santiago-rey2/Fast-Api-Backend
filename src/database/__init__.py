from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.core.config import settings

engine = create_engine(
    settings.sync_dsn, 
    echo=settings.sql_echo,
    pool_pre_ping=True, 
    pool_recycle=3600, 
    future=True
)

class Base(DeclarativeBase): 
    pass

SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False, 
    future=True
)

def init_db() -> None:
    """Initialize database tables and load default data"""
    # Import all models to register them with Base.metadata
    from src.entities import (
        plato, 
        vino, 
        categoria_plato, 
        categoria_vino,
        alergeno,
        bodega,
        denominacion_origen,
        enologo,
        uva,
        user
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Load default data
    _load_default_data()

def _load_default_data() -> None:
    """Load expanded default data into the database"""
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
        from src.auth.service import AuthService
        hashed_password = AuthService.get_password_hash("admin123")
        conn.execute(text("""
            INSERT IGNORE INTO users (username, email, hashed_password, is_active, is_admin) VALUES
            ('admin', 'admin@restaurant.com', :password, true, true)
        """), {"password": hashed_password})
        
        # === CATEGORÍAS DE PLATOS EXPANDIDAS ===
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
        
        # === BODEGAS BASE ===
        conn.execute(text("""
            INSERT IGNORE INTO bodegas (id, nombre, region) VALUES
            (0, 'Sin bodega', 'Sin región'),
            (1, 'Marqués de Riscal', 'Rioja'),
            (2, 'Vega Sicilia', 'Ribera del Duero'),
            (3, 'Torres', 'Penedès'),
            (4, 'Martín Códax', 'Rías Baixas'),
            (5, 'González Byass', 'Jerez'),
            (6, 'López de Heredia', 'Rioja'),
            (7, 'Muga', 'Rioja'),
            (8, 'CVNE', 'Rioja'),
            (9, 'Artadi', 'Rioja'),
            (10, 'Pingus', 'Ribera del Duero')
        """))
        
        # === ENÓLOGOS BASE ===
        conn.execute(text("""
            INSERT IGNORE INTO enologos (id, nombre) VALUES
            (0, 'Sin enólogo'),
            (1, 'Francisco Hurtado de Amézaga'),
            (2, 'Miguel Torres Maczassek'),
            (3, 'Pablo Álvarez'),
            (4, 'Mariano García'),
            (5, 'Telmo Rodríguez'),
            (6, 'María Vargas'),
            (7, 'Rafael Cambra'),
            (8, 'Alvaro Palacios'),
            (9, 'Jorge Ordóñez'),
            (10, 'Raúl Pérez')
        """))
        
        conn.commit()
        
        print("✅ Datos por defecto expandidos cargados correctamente")
        print("📊 Estructura completa disponible para la aplicación")
        print("👤 Usuario administrador creado:")
        print("   - Username: admin")
        print("   - Password: admin123")
        print("   - Email: admin@restaurant.com")

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()