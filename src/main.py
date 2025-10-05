"""
FastAPI Backend para gestión de carta de restaurante
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.database import init_db
from src.routes.public import router as public_router
from src.routes.admin import router as admin_router

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API de gestión para una carta de restaurante",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.env == "dev" else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(public_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")

# Inicializar base de datos
try:
    init_db()
except Exception as e:
    print(f"Error al inicializar la base de datos: {e}")

@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "message": "¡Bienvenido al API del Restaurante!",
        "version": "1.0.0",
        "documentation": "/docs"
    }
