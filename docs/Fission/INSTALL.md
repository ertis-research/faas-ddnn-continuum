# Fission service

> Las instrucciones originales están disponibles aquí:
> https://fission.io/docs/installation/#install-fission

```sh
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
# Nota: Ejecutar solo una vez
kubectl create -k "github.com/fission/fission/crds/v1?ref=v1.17.0"
helm repo add fission-charts https://fission.github.io/fission-charts/
helm repo update
helm install --version v1.17.0 --namespace $FISSION_NAMESPACE fission fission-charts/fission-all
```

# Fission CLI

```sh
curl -Lo fission https://github.com/fission/fission/releases/download/v1.17.0/fission-v1.17.0-linux-amd64
chmod +x fission
sudo mv fission /usr/local/bin/
```

# Próximos

```sh
# Add the stock NodeJS env to your Fission deployment
fission env create --name nodejs --image fission/node-env
# A javascript function that prints "hello world"
curl -LO https://raw.githubusercontent.com/fission/examples/main/nodejs/hello.js
# Upload your function code to fission
fission function create --name hello-js --env nodejs --code hello.js
# Test your function.  This takes about 100msec the first time.
fission function test --name hello-js
```

# Acceso externo.

## Ingress controller

> Las instrucciones completas están disponibles aquí
> https://fission.io/docs/usage/ingress/

<!-- TODO https://github.com/fission/fission/issues/2650 -->

```sh
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

# Dar de baja el servicio

## Fission

> Las instrucciones completas se encuentran aquí:
> https://fission.io/docs/installation/uninstallation/

````sh
helm uninstall fission -n fission
kubectl delete -k "github.com/fission/fission/crds/v1?ref=v1.17.0"
```

## Ingress controller

```sh
helm uninstall ingess-nginx -n fission
````
