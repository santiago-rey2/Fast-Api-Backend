"""
Script para crear la base de datos si no existe
"""
import sys
from sqlalchemy import create_engine, text
from src.core.config import settings

def create_database():
    """Crea la base de datos si no existe"""
    # Conexión sin especificar la base de datos
    base_dsn = (f"mysql+pymysql://{settings.db_user}:{settings.db_password}"
                f"@{settings.db_host}:{settings.db_port}/?charset=utf8mb4")
    
    engine = create_engine(base_dsn, echo=True)
    
    try:
        with engine.connect() as conn:
            # Verificar si la base de datos existe
            result = conn.execute(
                text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :db_name"),
                {"db_name": settings.db_name}
            )
            
            if result.fetchone() is None:
                # La base de datos no existe, crearla
                conn.execute(text(f"CREATE DATABASE {settings.db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                conn.commit()
                print(f"✅ Base de datos '{settings.db_name}' creada correctamente")
            else:
                print(f"ℹ️  La base de datos '{settings.db_name}' ya existe")
                
    except Exception as e:
        print(f"❌ Error creando la base de datos: {e}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    create_database()
