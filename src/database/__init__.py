from sqlalchemy import create_engine
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
    """Initialize database tables"""
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
    
    print("✅ Tablas de la base de datos creadas correctamente")

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()