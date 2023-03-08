Este documento sirve como guía de instalación de los componentes necesarios en
un cluster de Kubernetes para poder lanzar funciones serverless a través del
framework [OpenFaaS]

Los comandos de la guía están pensados para ser ejecutados en la carpeta actual
(`docs/OpenFaaS`), a no ser que se indique lo contrario

# OpenFaaS K8s

Instrucciones para la instalación de la plataforma OpenFaaS en un cluster de
Kubernetes.

> Las instalaciones originales están disponibles aquí:
> https://docs.openfaas.com/deployment/kubernetes/#2-deploy-the-openfaas-chart-with-helm

## Requisitos

- Cluster de Kubernetes
- [Helm]

## Instrucciones

> Estos comandos han sido probados en el nodo master (nodo1) en el cluster

```sh
# Crear los namespaces necesarios
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update
# Instalar OpenFaaS
helm upgrade openfaas --install openfaas/openfaas --namespace openfaas -f values.yml

# Aplicar parches
kubectl apply -f patch.yml
kubectl delete pod -l app=prometheus -n openfaas
```

# faas-cli

Instalación del CLI para gestionar un servicio OpenFaaS. Estas instrucciones
estan pensadas para instalar el CLI en un sistema Linux x64. Para otros sistemas
operativos, visite las instrucciones originales

> Las instalaciones originales están disponibles aquí:
> https://docs.openfaas.com/cli/install/#linux-or-macos

```sh
# Descargar el CLI
curl -sSL https://cli.openfaas.com | sudo -E sh
# Obtener la contraseña generada (usuario admin)
PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
echo "OpenFaaS admin password: $PASSWORD"
# Obtener la IP y puerto del gateway
kubectl get svc -n openfaas gateway-external -o wide
export OPENFAAS_URL=<HOST>:<PORT>

# Configurar el CLI
echo -n $PASSWORD | faas-cli login -g $OPENFAAS_URL -u admin --password-stdin
# Comprobar que el servicio está disponible
faas-cli version

# Opcional: Añadir autocompletado
echo 'source <(faas-cli completion --shell bash)' >>~/.bashrc
```

# Desinstalar OpenFaaS

## OpenFaaS K8s

```sh
helm uninstall openfaas -n openfaas
```

## faas-cli

```sh
rm `which faas-cli`
```

# Comprobar que el servicio funciona

Nos basta con obtener la versión del CLI. `faas-cli version`

<details>
<summary>Output</summary>

```txt
  ___                   _____           ____
 / _ \ _ __   ___ _ __ |  ___|_ _  __ _/ ___|
| | | | '_ \ / _ \ '_ \| |_ / _` |/ _` \___ \
| |_| | |_) |  __/ | | |  _| (_| | (_| |___) |
 \___/| .__/ \___|_| |_|_|  \__,_|\__,_|____/
      |_|

CLI:
 commit:  0074051aeb837f5f160ee8736341460468b5c190
 version: 0.15.4

Gateway
 uri:     http://node1:31112
 version: 0.25.2
 sha:     bc2eeff4678407583faec982c1c7d1da915dd60c


Provider
 name:          faas-netes
 orchestration: kubernetes
 version:       0.15.4
 sha:           330ac2a6d2e0db392a673b7fac97320d3e788139
```

</details>

[helm]: https://helm.sh/
[openfaas]: https://www.openfaas.com/
