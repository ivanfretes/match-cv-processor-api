#!/bin/bash

# Script para limpiar completamente Docker (contenedores, imágenes, volúmenes)
# Úsalo si tienes problemas persistentes con Docker

echo "🧹 Limpieza completa de Docker para este proyecto..."
echo "⚠️  Esto eliminará contenedores, imágenes y volúmenes relacionados"

read -p "¿Estás seguro? (s/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Operación cancelada"
    exit 1
fi

echo "  - Deteniendo y eliminando contenedores..."
docker-compose down -v --remove-orphans 2>/dev/null || true

echo "  - Eliminando contenedor fastapi-app..."
docker rm -f fastapi-app 2>/dev/null || true

echo "  - Eliminando imágenes del proyecto..."
docker images | grep -E "(match-cv-processor-api|fastapi-app)" | awk '{print $3}' | xargs docker rmi -f 2>/dev/null || true

echo "  - Limpiando volúmenes huérfanos..."
docker volume prune -f 2>/dev/null || true

echo "  - Limpiando redes huérfanas..."
docker network prune -f 2>/dev/null || true

echo "✅ Limpieza completada"
echo ""
echo "Ahora puedes ejecutar: ./init-local.sh"

