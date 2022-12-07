# OpenWhisk K8s

> Las instrucciones originales están disponibles en
> https://github.com/apache/openwhisk-deploy-kube/blob/master/README.md#overview

## Configurar los nodos

Es necesario indicar que nodos van a ser utilizados para lanzar funciones y
cuales usados para lanzar los elementos de control (couchdb, kafka, ...)

| Rol       | Desc                                      |
| --------- | ----------------------------------------- |
| invoker   | Ejecuta las funciones lambdas             |
| core      | Elementos de control (kafka, couchdb,...) |
| edge      | Nodos de acceso                           |
| providers | Event providers                           |

```sh
# Añadir label
kubectl label node <INVOKER_NODE_NAME> openwhisk-role=<ROLE>
# Borrar label
kubectl label node <INVOKER_NODE_NAME> openwhisk-role-
```

## Elegir los valores de la configuración

Para configurar el despliegue realizado por Helm, será necesario proporcionar un
fichero `values.yaml` con las opciones de configuración pertinentes

Para más información, consultar los siguientes enlaces

- Ejemplos de configuración:
  https://github.com/apache/openwhisk-deploy-kube/blob/master/deploy
- Opciones de configuración:
  https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/configurationChoices.md
- Valores por defecto:
  https://github.com/apache/openwhisk-deploy-kube/blob/master/helm/openwhisk/values.yaml

## Lanzar el servicio

```sh
helm repo add openwhisk https://openwhisk.apache.org/charts
helm repo update
# `--create-namespace` si no existe
helm install owdev openwhisk/openwhisk -n openwhisk -f values.yaml --create-namespace
```

# CLI

> Las instrucciones originales están disponibles en
> https://openwhisk.apache.org/documentation.html#wsk-cli

```sh
# Descargar la ultima versión del CLI para nuestro sistema desde
# https://github.com/apache/openwhisk-cli/releases
wget https://github.com/apache/openwhisk-cli/releases/download/1.2.0/OpenWhisk_CLI-1.2.0-linux-amd64.tgz
# Descomprimir el fichero
tar -xvf OpenWhisk_CLI-1.2.0-linux-amd64.tgz
# Mover el binario a una carpeta del PATH
sudo mv ./wsk /usr/local/bin/wsk

# Configuración del CLI

# Obtener el puerto correspondiente a 443 (HTTPs)
kubectl get service -n openwhisk
# Configurar el CLI
wsk property set --apihost <whisk.ingress.apiHostName>:<whisk.ingress.apiHostPort>
# Clave `whisk.auth.guest`
wsk property set --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
```

# Errores comunes de la instalación

Lista completa:
https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/troubleshooting.md

## `server gave http response to https client`

Estamos usando el puerto conectado al `80` del nginx. Revisar la configuración
de `wsk` y elegir el puerto correspondiente al `443`

<details>
<summary>Salida</summary>

```text
error: Unable to create action 'helloJS': Put "https://node1:32052/api/v1/namespaces/_/actions/helloJS?overwrite=false": http: server gave HTTP response to HTTPS client
Run 'wsk --help' for usage.
```

</details>

### Más información

- https://github.com/apache/openwhisk-deploy-kube/issues/165#issuecomment-373744280

## x509: certificate is not valid for any names, but wanted to match node1

El certificado instalado por Helm no coincide, es necesario añadir el argumento
`-i` para ignorar la comprobación

<details>
<summary>Salida</summary>

```text
error: Unable to create action 'helloJS': Put "https://node1:31001/api/v1/namespaces/_/actions/helloJS?overwrite=false": x509: certificate is not valid for any names, but wanted to match node1
Run 'wsk --help' for usage.
```

</details>

### Más información

- https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/troubleshooting.md#wsk-cannot-validate-certificates-error

## `ngnix host not found`

Esto ocurre porque el cluster de ERTIS está configurado para usar CoreDNS. Para
solucionarlo, basta con sustituir el valor de `k8s.dns` a `coredns.kube-system`

### Más información

- https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/troubleshooting.md#nginx-pod-fails-with-host-not-found-in-resolver-error
- https://github.com/apache/openwhisk-deploy-kube/issues/303#issuecomment-431287388

# Dar de baja el servicio

```sh
helm uninstall owdev -n openwhisk
```
