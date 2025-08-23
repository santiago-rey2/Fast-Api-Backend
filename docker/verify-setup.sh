#!/bin/bash
# Script de verificación de la infraestructura Docker

echo "🔍 Verificando infraestructura Docker..."

# Verificar que Docker esté funcionando
if ! docker --version >/dev/null 2>&1; then
    echo "❌ Docker no está disponible"
    exit 1
fi

echo "✅ Docker está disponible"

# Verificar archivos de configuración
echo "🔍 Verificando archivos de configuración..."

if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml encontrado"
else
    echo "❌ docker-compose.yml no encontrado"
    exit 1
fi

if [ -f "docker-compose.full.yml" ]; then
    echo "✅ docker-compose.full.yml encontrado"
else
    echo "❌ docker-compose.full.yml no encontrado"
    exit 1
fi

if [ -f "docker/.env.docker" ]; then
    echo "✅ docker/.env.docker encontrado"
else
    echo "❌ docker/.env.docker no encontrado"
    exit 1
fi

# Validar archivos docker-compose
echo "🔍 Validando sintaxis de docker-compose..."

if docker-compose config >/dev/null 2>&1; then
    echo "✅ docker-compose.yml es válido"
else
    echo "❌ Error en docker-compose.yml"
    docker-compose config
    exit 1
fi

if docker-compose -f docker-compose.full.yml config >/dev/null 2>&1; then
    echo "✅ docker-compose.full.yml es válido"
else
    echo "❌ Error en docker-compose.full.yml"
    docker-compose -f docker-compose.full.yml config
    exit 1
fi

# Verificar red Docker
echo "🔍 Verificando/creando red Docker..."
docker network create restaurante-network >/dev/null 2>&1 || echo "ℹ️  Red ya existe"

echo ""
echo "✅ Verificación completada exitosamente!"
echo ""
echo "🚀 Comandos para iniciar:"
echo "   Solo BD:        docker-compose up -d"
echo "   Sistema completo: docker-compose -f docker-compose.full.yml up -d"
echo "   Con script:     cd docker && ./start-docker.sh"
