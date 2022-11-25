# Function Mesh

> Las instalaciones originales están disponibles aquí:
> https://functionmesh.io/docs/install-function-mesh

## Instalar el gestor de certificados

```sh
helm repo add jetstack https://charts.jetstack.io
helm repo update
# `--create-namespace` si no existe `cert-manager`
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.8.0 \
  --set installCRDs=true
```

## Function Mesh Operator

```sh
helm repo add function-mesh http://charts.functionmesh.io/
helm repo update

export FUNCTION_MESH_RELEASE_NAME=function-mesh  # change the release name according to your scenario
export FUNCTION_MESH_RELEASE_NAMESPACE=function-mesh  # change the namespace to where you want to install Function Mesh

# `--create-namespace` si no existe `function-mesh`
helm install ${FUNCTION_MESH_RELEASE_NAME} function-mesh/function-mesh-operator -n ${FUNCTION_MESH_RELEASE_NAMESPACE} --create-namespace
```

---

# Borrar el servicio

```sh
helm uninstall function-mesh -n function-mesh
helm uninstall cert-manager -n cert-manager
```
