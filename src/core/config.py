from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal
from pathlib import Path

class Settings(BaseSettings):
    # Configuración de la aplicación
    app_name: str = Field(default="Restaurante API", env="APP_NAME")
    env: Literal["dev", "prod", "test"] = Field(default="dev", env="ENVIRONMENT")
    
    # Configuración de base de datos
    db_user: str = Field(env="DB_USER")
    db_password: str = Field(env="DB_PASSWORD")
    db_host: str = Field(default="127.0.0.1", env="DB_HOST")
    db_port: int = Field(default=3306, env="DB_PORT")
    db_name: str = Field(env="DB_NAME")
    sql_echo: bool = Field(default=False, env="SQL_ECHO")
    
    # Configuración JWT
    secret_key: str = Field(env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    @property
    def sync_dsn(self) -> str:
        return (f"mysql+pymysql://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4")

    model_config = {
        "env_file": Path(__file__).parent.parent.parent / ".env",  # Ruta absoluta al .env
        "extra": "ignore"
    }

settings = Settings()
