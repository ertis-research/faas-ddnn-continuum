# Apache pulsar Cluster

> Las instrucciones originales están disponibles aquí:
> https://pulsar.apache.org/docs/2.10.x/helm-install

## Preparar la instalación

Para preparar la instalación del cluster es necesario ejecutar un script
proporcionado por Pulsar, encargado de generar las claves publica/privada para
la autenticación, instalar plugins...

```sh
git clone https://github.com/apache/pulsar-helm-chart
cd pulsar-helm-chart
# NOTA: Añadir `-c` si no existe el namespace `pulsar` en Kubernetes
# NOTA: Comprobar usando `kubectl get namespaces | grep pulsar`
./scripts/pulsar/prepare_helm_release.sh -n pulsar -k pulsar
```

<details>

<summary>Salida</summary>

```
ertis@node1:~/altair/pulsar-helm-chart$ ./scripts/pulsar/prepare_helm_release.sh -n pulsar -k pulsar
generate the token keys for the pulsar cluster
The private key and public key are generated to /tmp/tmp.ImyWhMgcFd and /tmp/tmp.5NVruoNgNK successfully.
secret/pulsar-token-asymmetric-key created
generate the tokens for the super-users: proxy-admin,broker-admin,admin
generate the token for proxy-admin
pulsar-token-asymmetric-key
kubectl get -n pulsar secrets pulsar-token-asymmetric-key -o jsonpath={.data.PRIVATEKEY} | base64 --decode > /tmp/tmp.ANyvZGbHMt
secret/pulsar-token-proxy-admin created
generate the token for broker-admin
pulsar-token-asymmetric-key
kubectl get -n pulsar secrets pulsar-token-asymmetric-key -o jsonpath={.data.PRIVATEKEY} | base64 --decode > /tmp/tmp.fxHsQiKapx
secret/pulsar-token-broker-admin created
generate the token for admin
pulsar-token-asymmetric-key
kubectl get -n pulsar secrets pulsar-token-asymmetric-key -o jsonpath={.data.PRIVATEKEY} | base64 --decode > /tmp/tmp.hMqLqKgmhs
secret/pulsar-token-admin created
-------------------------------------

The jwt token secret keys are generated under:
    - 'pulsar-token-asymmetric-key'

The jwt tokens for superusers are generated and stored as below:
    - 'proxy-admin':secret('pulsar-token-proxy-admin')
    - 'broker-admin':secret('pulsar-token-broker-admin')
    - 'admin':secret('pulsar-token-admin')

```

</details>

## Instalar Pulsar

La instalación de Apache Pulsar se realiza a través de `helm`

> Todas las opciones de configuración están disponibles aquí:
> https://github.com/apache/pulsar-helm-chart/blob/master/charts/pulsar/values.yaml

```sh
helm repo add apache https://pulsar.apache.org/charts
helm repo update
# Nota: Puede tardar mucho tiempo
helm install pulsar apache/pulsar --timeout 20m --namespace pulsar -f values.yaml
```

# Pulsar CLI Tools

> Las instrucciones originales están disponibles aquí
> https://pulsar.apache.org/docs/2.10.x/getting-started-helm

La gestión de Pulsar se realiza a través de utilidades CLI disponibles para su
descarga desde la web oficial. Las utilidades requieren de un Java JDK 17
instalado o superior

```sh
wget https://archive.apache.org/dist/pulsar/pulsar-2.10.2/apache-pulsar-2.10.2-bin.tar.gz
tar xvfz apache-pulsar-2.10.2-bin.tar.gz
# La carpeta apache-pulsar-2.10.2 contiene los archivos necesarios para
# ejecutar las CLI tools de Pulsar (situadas en dentro de `bin/`)
cd apache-pulsar-2.10.2
```

Es necesario añadir la siguiente variable de entorno en el `.bashrc`

```sh
export PULSAR_HOME=<PATH_APACHE_PULSAR_INFLATED_TARBAL_DIR>
```

## Configuración de las CLI tools

### Configurar el acceso al cluster de Pulsar

Dentro de la carpeta `$PULSAR_HOME/conf`, existe un fichero `client.conf` que
permite configurar las opciones de conexión de las CLI tools

```conf
webServiceUrl=http://node1:<NODE_PORT_HTTP_PROXY_SERVICE>/
brokerServiceUrl=pulsar://node1:<NODE_PORT_HTTP_PROXY_SERVICE>/
```

<details>
  <summary>Conocer el valor NODE_PORT_HTTP_PROXY_SERVICE</summary>

```txt
ertis@node1:~/altair/apache-pulsar-2.10.2$ kubectl --namespace=pulsar describe service pulsar-proxy
Name:                     pulsar-proxy
Namespace:                pulsar
Labels:                   app=pulsar
                          app.kubernetes.io/managed-by=Helm
                          chart=pulsar-3.0.0
                          cluster=pulsar
                          component=proxy
                          heritage=Helm
                          release=pulsar
Annotations:              meta.helm.sh/release-name: pulsar
                          meta.helm.sh/release-namespace: pulsar
Selector:                 app=pulsar,component=proxy,release=pulsar
Type:                     LoadBalancer
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.10.33.229
IPs:                      10.10.33.229
Port:                     http  80/TCP
TargetPort:               80/TCP
NodePort:                 http  30669/TCP
Endpoints:                10.10.34.200:80,10.10.34.54:80,10.10.34.85:80
Port:                     pulsar  6650/TCP
TargetPort:               6650/TCP
NodePort:                 pulsar  31225/TCP
Endpoints:                10.10.34.200:6650,10.10.34.54:6650,10.10.34.85:6650
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

</details>

# Próximos pasos

1. Verificar el funcionamiento del cluster:
   https://pulsar.apache.org/docs/next/getting-started-helm/#step-2-use-pulsar-admin-to-create-pulsar-tenantsnamespacestopics
2. Verificar el acceso desde el exterior del cluster

```sh
bin/pulsar-admin tenants list
```

3. Verificar que se pueden crear funciones de Pulsar:
   https://pulsar.apache.org/docs/next/getting-started-helm/#step-2-use-pulsar-admin-to-create-pulsar-tenantsnamespacestopics

4. Instalar un conector para generar datos en los topics:
   https://pulsar.apache.org/docs/2.10.x/io-use/

---

# Borrar el servicio

```sh
helm uninstall pulsar -n pulsar
```
