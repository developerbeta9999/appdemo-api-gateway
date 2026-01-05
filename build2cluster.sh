#!/bin/bash

# --- CONFIGURACIÓN ---
SERVICE_NAME="api-gateway"
IMAGE_NAME="appdemo-images/api-gateway:v1" # Debe coincidir con tu YAML en k8s
CLUSTER_NAME="cluster-appdemo" # Nombre definido en k3d-config.yaml [cite: 20]
NAMESPACE="appdemo"

# Detener el script si hay errores
set -e

# 0. ASEGURAR UBICACIÓN
# Esto mueve la terminal a la carpeta donde está guardado este archivo .sh
# Garantiza que el comando docker build encuentre el Dockerfile en "."
cd "$(dirname "$0")"

echo "========================================"
echo "🚪 Iniciando Build para: $SERVICE_NAME"
echo "========================================"

# 1. CONSTRUIR IMAGEN DOCKER
# Usamos "." porque ya estamos dentro de la carpeta del api-gateway
echo "🐳 Construyendo imagen Docker: $IMAGE_NAME..."
docker build -t $IMAGE_NAME .

# 2. IMPORTAR A K3D
echo "📥 Inyectando imagen al clúster K3d..."
k3d image import $IMAGE_NAME -c $CLUSTER_NAME