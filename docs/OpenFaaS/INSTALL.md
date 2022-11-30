# faas-cli

> Las instalaciones originales están disponibles aquí:
> https://docs.openfaas.com/cli/install/#linux-or-macos

```sh
curl -sSL https://cli.openfaas.com | sudo -E sh
faas-cli version
# Opcional: Añadir autocompletado
echo 'source <(faas-cli completion --shell bash)' >>~/.bashrc
```

# OpenFaaS

> Las instalaciones originales están disponibles aquí:
> https://docs.openfaas.com/deployment/kubernetes/#2-deploy-the-openfaas-chart-with-helm

```sh
# Crear los namespaces necesarios
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update
# Instalar OpenFaaS
helm upgrade openfaas --install openfaas/openfaas \
  --namespace openfaas  \
  --set functionNamespace=openfaas-fn \
  --set generateBasicAuth=true
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
```

<details>
<summary>`faas-cli version`</summary>

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
