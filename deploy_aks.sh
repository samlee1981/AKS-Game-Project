#!/bin/bash

# Stop on error
set -e

echo "Starting deployment process..."

# Check prerequisites
if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI (az) is not installed."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "Error: docker is not installed."
    exit 1
fi

# Ask for user input
read -p "Enter your Azure Container Registry (ACR) name (e.g., myacr): " ACR_NAME
read -p "Enter your Resource Group name: " RESOURCE_GROUP
read -p "Enter your AKS Cluster name: " AKS_CLUSTER

if [ -z "$ACR_NAME" ] || [ -z "$RESOURCE_GROUP" ] || [ -z "$AKS_CLUSTER" ]; then
    echo "Error: All fields are required."
    exit 1
fi

ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"
IMAGE_NAME="${ACR_LOGIN_SERVER}/game-center:v1"

echo "--------------------------------------------------"
echo "Configuration:"
echo "ACR: $ACR_LOGIN_SERVER"
echo "Resource Group: $RESOURCE_GROUP"
echo "AKS Cluster: $AKS_CLUSTER"
echo "Image: $IMAGE_NAME"
echo "--------------------------------------------------"

# Login to ACR
echo "Logging in to ACR..."
az acr login --name "$ACR_NAME"

# Get AKS credentials
echo "Getting AKS credentials..."
az aks get-credentials --resource-group "$RESOURCE_GROUP" --name "$AKS_CLUSTER" --overwrite-existing

# Build Docker image
echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

# Push Docker image
echo "Pushing Docker image to ACR..."
docker push "$IMAGE_NAME"

# Prepare Kubernetes manifest
echo "Generating Kubernetes manifest..."
sed "s|REPLACE_ME_IMAGE_NAME|$IMAGE_NAME|g" Yaml/combined-game.yaml > deployment_final.yaml

# Apply to AKS
echo "Deploying to AKS..."
kubectl apply -f deployment_final.yaml

echo "--------------------------------------------------"
echo "Deployment applied successfully!"
echo "Check your services with: kubectl get svc"
echo "Check your pods with: kubectl get pods"
echo "--------------------------------------------------"
