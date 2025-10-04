"""
FastAPI Backend para gestión de carta de restaurante
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.database import init_db
from src.routes.public import router as menu_routes
from src.routes.admin import router as admin_routes

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API de gestión para una carta de restaurante común",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware de seguridad para hosts confiables
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"] if settings.env == "dev" else ["localhost", "127.0.0.1"]
)

# Configurar CORS con headers adicionales para manejar upgrade-insecure-requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.env == "dev" else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "*",
        "upgrade-insecure-requests",
        "content-security-policy",
        "x-requested-with"
    ],
)

# Middleware personalizado para manejar headers de seguridad
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Headers de seguridad para desarrollo
    if settings.env == "dev":
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:; "
            "connect-src 'self' http: https:; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:;"
        )
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response

app.include_router(menu_routes, prefix="/api/v1")
app.include_router(admin_routes, prefix="/api/v1")

# Inicializar base de datos en desarrollo
if settings.env == "dev":
    try:
        init_db()
        
        # Cargar datos de ejemplo automáticamente desde el script
        try:
            import sys
            from pathlib import Path
            
            # Agregar scripts-examples al path
            scripts_path = Path("scripts-examples")
            if scripts_path.exists():
                sys.path.insert(0, str(scripts_path))
                
                # Importar y ejecutar la función de carga automática
                from load_sample_data import load_sample_data_auto
                load_sample_data_auto()
                
        except ImportError as e:
            print(f"⚠️  No se pudo cargar el módulo de datos de ejemplo: {e}")
        except Exception as sample_error:
            print(f"⚠️  Error cargando datos de ejemplo: {sample_error}")
                
    except Exception as e:
        print(f"Error inicializando BD: {e}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "error": str(exc) if settings.env == "dev" else "Error interno"
        }
    )

@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "message": "¡Bienvenido al API del Restaurante!",
        "version": "1.0.0",
        "documentation": "/docs"
    }
