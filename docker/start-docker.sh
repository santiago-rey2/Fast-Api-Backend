#!/bin/bash
# Script para inicializar la infraestructura Docker

echo "🐳 Iniciando infraestructura Docker para FastAPI Restaurant Backend..."

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instálalo primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instálalo primero."
    exit 1
fi

# Crear red si no existe
echo "🌐 Creando red Docker..."
docker network create restaurante-network 2>/dev/null || true

# Cargar variables de entorno
if [ -f "docker/.env.docker" ]; then
    echo "📋 Cargando configuración de Docker..."
    export $(cat docker/.env.docker | grep -v '^#' | xargs)
else
    echo "⚠️  Archivo docker/.env.docker no encontrado. Usando valores por defecto."
fi

# Opción 1: Solo base de datos
echo ""
echo "Selecciona una opción:"
echo "1) Solo base de datos MySQL"
echo "2) Aplicación completa (MySQL + FastAPI + Adminer)"
echo "3) Salir"
read -p "Opción [1-3]: " option

case $option in
    1)
        echo "🗄️  Iniciando solo base de datos MySQL..."
        docker-compose up -d mysql-db adminer
        ;;
    2)
        echo "🚀 Iniciando aplicación completa..."
        docker-compose -f docker-compose.full.yml up -d
        ;;
    3)
        echo "👋 Saliendo..."
        exit 0
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "✅ Infraestructura iniciada correctamente!"
echo ""
echo "📍 Servicios disponibles:"
echo "   🗄️  MySQL: localhost:3306"
echo "   🌐 Adminer: http://localhost:8080"

if [ "$option" = "2" ]; then
    echo "   🚀 FastAPI: http://localhost:8000"
    echo "   📚 Docs: http://localhost:8000/docs"
fi

echo ""
echo "🔧 Comandos útiles:"
echo "   docker-compose logs -f          # Ver logs"
echo "   docker-compose down             # Detener servicios"
echo "   docker-compose down -v          # Detener y eliminar volúmenes"
echo "   docker-compose restart          # Reiniciar servicios"
