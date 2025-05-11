#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Starting Incident Framework deployment...${NC}"

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo -e "${RED}Docker is required but not installed. Aborting.${NC}" >&2; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo -e "${RED}kubectl is required but not installed. Aborting.${NC}" >&2; exit 1; }

# Create monitoring namespace
echo -e "${GREEN}Creating monitoring namespace...${NC}"
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Build and push Docker images
echo -e "${GREEN}Building Docker images...${NC}"
docker build -t incident-framework/alert-manager:latest ./alerting

# Apply Kubernetes manifests
echo -e "${GREEN}Deploying to Kubernetes...${NC}"
kubectl apply -f kubernetes/alert-manager.yaml

# Wait for deployments to be ready
echo -e "${GREEN}Waiting for deployments to be ready...${NC}"
kubectl rollout status deployment/alert-manager -n monitoring

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "You can now use the incident-framework CLI to manage incidents."
echo -e "Try running: incident-framework --help" 