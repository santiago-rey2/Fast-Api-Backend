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
    """Load default data into the database"""
    with engine.connect() as conn:
        # Configurar modo SQL para permitir ID 0
        conn.execute(text("SET SESSION sql_mode = 'NO_AUTO_VALUE_ON_ZERO'"))
        
        # Verificar si ya existen datos (para evitar duplicados)
        result = conn.execute(text("SELECT COUNT(*) FROM categoria_platos"))
        if result.scalar() > 0:
            print("ℹ️  Los datos por defecto ya están cargados")
            return
        
        print("🌱 Cargando datos por defecto...")
        
        # Crear usuario administrador por defecto
        from src.auth.service import AuthService
        hashed_password = AuthService.get_password_hash("admin123")
        conn.execute(text("""
            INSERT IGNORE INTO users (username, email, hashed_password, is_active, is_admin) VALUES
            ('admin', 'admin@restaurant.com', :password, true, true)
        """), {"password": hashed_password})
        
        # Categorías de platos por defecto
        conn.execute(text("""
            INSERT IGNORE INTO categoria_platos (id, nombre) VALUES
            (0, 'Sin categoría'),
            (1, 'Entrantes'),
            (2, 'Platos principales'), 
            (3, 'Postres'),
            (4, 'Ensaladas'),
            (5, 'Tapas'),
            (6, 'Arroces'),
            (7, 'Carnes'),
            (8, 'Pescados'),
            (9, 'Mariscos')
        """))
        
        # Los 14 alérgenos según la ley española
        conn.execute(text("""
            INSERT IGNORE INTO alergenos (id, nombre) VALUES
            (0, 'Sin alérgenos'),
            (1, 'Cereales que contienen gluten'),
            (2, 'Crustáceos'),
            (3, 'Huevos'),
            (4, 'Pescado'),
            (5, 'Cacahuetes'),
            (6, 'Soja'),
            (7, 'Leche'),
            (8, 'Frutos de cáscara'),
            (9, 'Apio'),
            (10, 'Mostaza'),
            (11, 'Granos de sésamo'),
            (12, 'Dióxido de azufre y sulfitos'),
            (13, 'Altramuces'),
            (14, 'Moluscos')
        """))
        
        # Categorías de vinos por defecto
        conn.execute(text("""
            INSERT IGNORE INTO categoria_vinos (id, nombre) VALUES
            (0, 'Sin categoría'),
            (1, 'Tinto joven'),
            (2, 'Tinto crianza'),
            (3, 'Tinto reserva'),
            (4, 'Tinto gran reserva'),
            (5, 'Blanco joven'),
            (6, 'Blanco fermentado en barrica'),
            (7, 'Rosado'),
            (8, 'Espumoso'),
            (9, 'Dulce'),
            (10, 'Generoso')
        """))
        
        # Denominaciones de origen básicas
        conn.execute(text("""
            INSERT IGNORE INTO denominaciones_origen (id, nombre, region) VALUES
            (0, 'Sin D.O.', 'sin especificar'),
            (1, 'D.O. Rioja', 'La Rioja'),
            (2, 'D.O. Ribera del Duero', 'Castilla y León'),
            (3, 'D.O. Penedès', 'Cataluña'),
            (4, 'D.O. Rías Baixas', 'Galicia'),
            (5, 'D.O. Jerez', 'Andalucía')
        """))
        
        # Tipos de uva comunes
        conn.execute(text("""
            INSERT IGNORE INTO uvas (id, nombre, tipo) VALUES
            (0, 'Sin uva', 'Sin tipo'),
            (1, 'Tempranillo', 'Tinta'),
            (2, 'Garnacha', 'Tinta'),
            (3, 'Albariño', 'Blanca'),
            (4, 'Verdejo', 'Blanca'),
            (5, 'Chardonnay', 'Blanca'),
            (6, 'Cabernet Sauvignon', 'Tinta'),
            (7, 'Merlot', 'Tinta'),
            (8, 'Sauvignon Blanc', 'Blanca'),
            (9, 'Monastrell', 'Tinta'),
            (10, 'Bobal', 'Tinta')
        """))
        
        conn.commit()
        print("✅ Datos por defecto cargados correctamente")
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