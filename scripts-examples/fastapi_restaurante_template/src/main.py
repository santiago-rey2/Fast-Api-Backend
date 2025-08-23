from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.database import init_db
from src.api.v1 import platos, vinos

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código al iniciar
    if settings.env == "dev":
      #  init_db()
      pass
    yield
    # Código al cerrar (ej. cerrar conexiones, limpiar cache)

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(platos.router, prefix="/api/v1")
app.include_router(vinos.router, prefix="/api/v1")
