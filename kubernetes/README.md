# Kubernetes Deployment

This directory contains manifests for deploying the alert manager and related components.

- `alert-manager.yaml`: Deployment, Service, and NetworkPolicy for the alert manager
- `rbac.yaml`: RBAC policies for secure operation

Apply all manifests with:

```bash
kubectl apply -f rbac.yaml
kubectl apply -f alert-manager.yaml
``` 