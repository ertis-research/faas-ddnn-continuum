Este documento sirve como guía de instalación de los componentes necesarios en
un cluster de Kubernetes para poder lanzar funciones serverless a través del
framework [Fission]

Los comandos de la guía están pensados para ser ejecutados en la carpeta actual
(`docs/Fission`), a no ser que se indique lo contrario

# Fission K8s

Instrucciones para la instalación de la plataforma Fission en un cluster de
Kubernetes. Esta guía activa las siguientes funciones extras:

- Permite crear triggers HTTP a través de un [Ingress Controller]
- Permite crear triggers a través de Kafka, RabbitMQ, etc a través de [KEDA]

> Las instrucciones originales están disponibles aquí:
> https://fission.io/docs/installation/#install-fission

## Requisitos

Es necesario tener instalados los siguientes componentes en el cluster de
Kubernetes. Se proporcionan guías de instalación de estos componentes en la
carpeta `/docs`

- Cluster de Kubernetes
- [Helm]
- [KEDA]
- [Ingress Controller]

## Instrucciones

> Estos comandos han sido probados en el nodo master (nodo1) en el cluster

```sh
export FISSION_NAMESPACE="fission"
# Si no existe el namespace
kubectl create namespace $FISSION_NAMESPACE
kubectl create -k "github.com/fission/fission/crds/v1?ref=v1.18.0"
helm repo add fission-charts https://fission.github.io/fission-charts/
helm repo update
helm install --version v1.18.0 -f values.yaml --namespace $FISSION_NAMESPACE fission fission-charts/fission-all
```

# Fission CLI

Instalación del CLI para gestionar un servicio Fission. Estas instrucciones
estan pensadas para instalar el CLI en un sistema Linux x64. Para otros sistemas
operativos, visite las instrucciones originales

> Las instrucciones originales están disponibles aquí:
> https://fission.io/docs/installation/#install-fission-cli

## Instrucciones

> Estos comandos han sido probados en el nodo master (nodo1) del cluster

```sh
curl -Lo fission https://github.com/fission/fission/releases/download/v1.17.0/fission-v1.17.0-linux-amd64
chmod +x fission
sudo mv fission /usr/local/bin/
```

# Desinstalar Fission

## Fission K8s

> Las instrucciones originales están disponibles aquí:
> https://fission.io/docs/installation/uninstallation/

```sh
helm uninstall fission -n fission
kubectl delete -k "github.com/fission/fission/crds/v1?ref=v1.17.0"
```

## Fission CLI

```sh
rm `which fission`
```

---

# Comprobar que el servicio funciona

Los siguientes comandos despliegan una función simple de NodeJS

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

[ingress controller]:
  https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers
[keda]: https://keda.sh/
[fission]: https://fission.io/
[helm]: https://helm.sh/
