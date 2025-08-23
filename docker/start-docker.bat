@echo off
REM Script para inicializar la infraestructura Docker en Windows

echo 🐳 Iniciando infraestructura Docker para FastAPI Restaurant Backend...

REM Verificar que Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está instalado. Por favor instálalo primero.
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose no está instalado. Por favor instálalo primero.
    exit /b 1
)

REM Crear red si no existe
echo 🌐 Creando red Docker...
docker network create restaurante-network >nul 2>&1

REM Verificar archivo de configuración
if exist "docker\.env.docker" (
    echo 📋 Configuración encontrada en docker\.env.docker
) else (
    echo ⚠️  Archivo docker\.env.docker no encontrado. Usando valores por defecto.
)

echo.
echo Selecciona una opción:
echo 1^) Solo base de datos MySQL
echo 2^) Aplicación completa ^(MySQL + FastAPI + Adminer^)
echo 3^) Salir
set /p option="Opción [1-3]: "

if "%option%"=="1" (
    echo 🗄️  Iniciando solo base de datos MySQL...
    docker-compose --env-file docker\.env.docker up -d mysql-db adminer
) else if "%option%"=="2" (
    echo 🚀 Iniciando aplicación completa...
    docker-compose --env-file docker\.env.docker -f docker-compose.full.yml up -d
) else if "%option%"=="3" (
    echo 👋 Saliendo...
    exit /b 0
) else (
    echo ❌ Opción inválida
    exit /b 1
)

echo.
echo ✅ Infraestructura iniciada correctamente!
echo.
echo 📍 Servicios disponibles:
echo    🗄️  MySQL: localhost:3306
echo    🌐 Adminer: http://localhost:8080

if "%option%"=="2" (
    echo    🚀 FastAPI: http://localhost:8000
    echo    📚 Docs: http://localhost:8000/docs
)

echo.
echo 🔧 Comandos útiles:
echo    docker-compose logs -f          # Ver logs
echo    docker-compose down             # Detener servicios
echo    docker-compose down -v          # Detener y eliminar volúmenes
echo    docker-compose restart          # Reiniciar servicios

pause
