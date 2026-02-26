# Stop on error
$ErrorActionPreference = "Stop"

Write-Host "Starting deployment process..."

# Check prerequisites
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Azure CLI (az) is not installed."
    exit 1
}

if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "Error: kubectl is not installed."
    exit 1
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: docker is not installed."
    exit 1
}

# Ask for user input
$ACR_NAME = Read-Host "Enter your Azure Container Registry (ACR) name (e.g., myacr)"
$RESOURCE_GROUP = Read-Host "Enter your Resource Group name"
$AKS_CLUSTER = Read-Host "Enter your AKS Cluster name"

if ([string]::IsNullOrWhiteSpace($ACR_NAME) -or [string]::IsNullOrWhiteSpace($RESOURCE_GROUP) -or [string]::IsNullOrWhiteSpace($AKS_CLUSTER)) {
    Write-Host "Error: All fields are required."
    exit 1
}

$ACR_LOGIN_SERVER = "$ACR_NAME.azurecr.io"
$IMAGE_NAME = "$ACR_LOGIN_SERVER/game-center:v1"

Write-Host "--------------------------------------------------"
Write-Host "Configuration:"
Write-Host "ACR: $ACR_LOGIN_SERVER"
Write-Host "Resource Group: $RESOURCE_GROUP"
Write-Host "AKS Cluster: $AKS_CLUSTER"
Write-Host "Image: $IMAGE_NAME"
Write-Host "--------------------------------------------------"

# Login to ACR
Write-Host "Logging in to ACR..."
az acr login --name $ACR_NAME

# Get AKS credentials
Write-Host "Getting AKS credentials..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --overwrite-existing

# Build Docker image
Write-Host "Building Docker image..."
docker build -t $IMAGE_NAME .

# Push Docker image
Write-Host "Pushing Docker image to ACR..."
docker push $IMAGE_NAME

# Prepare Kubernetes manifest
Write-Host "Generating Kubernetes manifest..."
(Get-Content "Yaml/combined-game.yaml") -replace 'REPLACE_ME_IMAGE_NAME', $IMAGE_NAME | Set-Content "deployment_final.yaml"

# Apply to AKS
Write-Host "Deploying to AKS..."
kubectl apply -f deployment_final.yaml

Write-Host "--------------------------------------------------"
Write-Host "Deployment applied successfully!"
Write-Host "Check your services with: kubectl get svc"
Write-Host "Check your pods with: kubectl get pods"
Write-Host "--------------------------------------------------"
