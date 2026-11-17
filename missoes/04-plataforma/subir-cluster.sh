#!/usr/bin/env bash
# Cria um Kubernetes local (kind) e aplica a loja quebrada.
set -euo pipefail
kind get clusters | grep -qx modo-carreira || kind create cluster --name modo-carreira --wait 120s
kubectl apply -f "$(dirname "$0")/k8s/"
echo "Cluster no ar. Agora investigue: kubectl get pods -n loja"
