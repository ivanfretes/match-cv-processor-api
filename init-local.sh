#!/bin/bash

# Script para iniciar el proyecto localmente con Docker Compose
# Este script limpia contenedores e imágenes existentes antes de iniciar

# No usar set -e aquí porque algunos comandos de limpieza pueden fallar legítimamente
# set -e  # Salir si hay algún error

echo "🧹 Limpiando contenedores e imágenes existentes..."

# Detener contenedores existentes (ignorar errores si no existen)
echo "  - Deteniendo contenedores..."
docker-compose down -v 2>/dev/null || true

# Eliminar el contenedor específico si existe (forzar eliminación)
echo "  - Eliminando contenedor fastapi-app..."
docker rm -f fastapi-app 2>/dev/null || true

# Eliminar cualquier contenedor que contenga "fastapi" en su nombre
echo "  - Eliminando contenedores relacionados con fastapi..."
for container_id in $(docker ps -a --filter "name=fastapi" --format "{{.ID}}" 2>/dev/null); do
    docker rm -f "$container_id" 2>/dev/null || true
done

# Limpiar cualquier contenedor detenido relacionado
echo "  - Limpiando contenedores huérfanos..."
docker container prune -f 2>/dev/null || true

# Limpiar volúmenes huérfanos (opcional, más agresivo)
echo "  - Limpiando volúmenes huérfanos..."
docker volume prune -f 2>/dev/null || true

# Si hay problemas con imágenes corruptas, reconstruir forzando
echo "  - Verificando y limpiando imágenes..."
for img_id in $(docker images "match-cv-processor-api*" --format "{{.ID}}" 2>/dev/null); do
    echo "    - Eliminando imagen: $img_id"
    docker rmi -f "$img_id" 2>/dev/null || true
done

echo "✅ Limpieza completada"
echo ""
echo "🔑 Configurando variables de entorno..."

# Exportar la API key de OpenAI
# Nota: Por seguridad, considera usar un archivo .env en lugar de hardcodear aquí
export OPENAI_API_KEY="${OPENAI_API_KEY:-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}"
export OPENAI_MODEL="${OPENAI_MODEL:-gpt-3.5-turbo}"

echo "🚀 Iniciando aplicación con Docker Compose..."
echo ""

# Construir e iniciar los contenedores
# Usar --build para forzar reconstrucción si es necesario
set -e  # Activar error checking solo para los comandos críticos
docker-compose up --build

