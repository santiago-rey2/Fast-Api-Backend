"""
FastAPI Backend para gestión de carta de restaurante
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.database import init_db
from src.routes.platos import router as platos_router
from src.routes.vinos import router as vinos_router
from src.routes.admin import router as admin_router
from src.routes.auth import router as auth_router

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

# Inicializar base de datos en desarrollo
if settings.env == "dev":
    try:
        init_db()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"⚠️  Error inicializando base de datos: {e}")

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
        "app_name": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "environment": settings.env,
        "public_endpoints": {
            "platos": "/api/v1/platos",
            "vinos": "/api/v1/vinos"
        },
        "auth_endpoints": {
            "login": "/api/v1/auth/login",
            "register": "/api/v1/auth/register"
        },
        "admin_endpoints": {
            "administration": "/api/v1/admin",
            "user_management": "/api/v1/auth/users"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint de salud de la aplicación"""
    return {"status": "healthy", "environment": settings.env}

# Incluir routers de la API
app.include_router(platos_router, prefix="/api/v1")
app.include_router(vinos_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app", 
        host="127.0.0.1",  # Cambiar a localhost específicamente
        port=8000, 
        reload=True,
        log_level="info"
    )
