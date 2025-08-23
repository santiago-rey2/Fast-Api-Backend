from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal

class Settings(BaseSettings):
    app_name: str = Field(default="Restaurante API")
    env: Literal["dev", "prod", "test"] = "dev"
    db_user: str = "root"
    db_password: str = "123456789"
    db_host: str = "127.0.0.1"
    db_port: int = 9000
    db_name: str = "restaurante_db"
    sql_echo: bool = True
    
    # Configuración JWT
    secret_key: str = Field(default="your-secret-key-change-in-production-very-long-and-secure")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def sync_dsn(self) -> str:
        return (f"mysql+pymysql://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4")

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
