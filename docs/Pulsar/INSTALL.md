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
./scripts/pulsar/prepare_helm_release.sh -n pulsar -k apache/pulsar
```

<details>

<summary>Salida</summary>

```
ertis@node1:~/altair/pulsar-helm-chart$ ./scripts/pulsar/prepare_helm_release.sh -n pulsar -k apache/pulsar -c
namespace/pulsar created
generate the token keys for the pulsar cluster
Get pulsarctl install.sh script ...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3987  100  3987    0     0   7329      0 --:--:-- --:--:-- --:--:--  7329
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 6835k  100 6835k    0     0  2310k      0  0:00:02  0:00:02 --:--:-- 3459k
~/altair/pulsar-helm-chart/pulsarctl-amd64-linux ~/altair/pulsar-helm-chart
The plugins of pulsarctl v0.4.0 are successfully installed under directory '/home/ertis/.pulsarctl/plugins'.

In order to use this plugins, please add the plugin directory '/home/ertis/.pulsarctl/plugins' to the system PATH. You can do so by adding the following line to your bash profile.

export PATH=${PATH}:${HOME}/.pulsarctl/plugins

Happy Pulsaring!
~/altair/pulsar-helm-chart
The private key and public key are generated to /tmp/tmp.G0jynXP4Lx and /tmp/tmp.cgoPV48gEX successfully.
error: failed to create secret Secret "apache/pulsar-token-asymmetric-key" is invalid: metadata.name: Invalid value: "apache/pulsar-token-asymmetric-key": a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*')
generate the tokens for the super-users: proxy-admin,broker-admin,admin
generate the token for proxy-admin
apache/pulsar-token-asymmetric-key
kubectl get -n pulsar secrets apache/pulsar-token-asymmetric-key -o jsonpath={.data.PRIVATEKEY} | base64 --decode > /tmp/tmp.DRVVURd1M0
error: there is no need to specify a resource type as a separate argument when passing arguments in resource/name form (e.g. 'kubectl get resource/<resource_name>' instead of 'kubectl get resource resource/<resource_name>'
generate the token for broker-admin
apache/pulsar-token-asymmetric-key
kubectl get -n pulsar secrets apache/pulsar-token-asymmetric-key -o jsonpath={.data.PRIVATEKEY} | base64 --decode > /tmp/tmp.iiEsYTUyiu
error: there is no need to specify a resource type as a separate argument when passing arguments in resource/name form (e.g. 'kubectl get resource/<resource_name>' instead of 'kubectl get resource resource/<resource_name>'
generate the token for admin
apache/pulsar-token-asymmetric-key
kubectl get -n pulsar secrets apache/pulsar-token-asymmetric-key -o jsonpath={.data.PRIVATEKEY} | base64 --decode > /tmp/tmp.imitOhi1oY
error: there is no need to specify a resource type as a separate argument when passing arguments in resource/name form (e.g. 'kubectl get resource/<resource_name>' instead of 'kubectl get resource resource/<resource_name>'
-------------------------------------

The jwt token secret keys are generated under:
    - 'apache/pulsar-token-asymmetric-key'

The jwt tokens for superusers are generated and stored as below:
    - 'proxy-admin':secret('apache/pulsar-token-proxy-admin')
    - 'broker-admin':secret('apache/pulsar-token-broker-admin')
    - 'admin':secret('apache/pulsar-token-admin')
```

</details>

## Instalar Pulsar

La instalación de Apache Pulsar se realiza a través de `helm`

```sh
helm repo add apache https://pulsar.apache.org/charts
helm repo update
# Nota: Puede tardar mucho tiempo
helm install pulsar apache/pulsar \
  --timeout 20m \
  # Inicializar el volumen
  --set initialize=true \
  # Desactivar la persistencia de datos. Consultar documentación
  --set volumes.persistence=false
```

# Pulsar CLI Tools

> Las instrucciones originales están disponibles aquí
> https://pulsar.apache.org/docs/2.10.x/getting-started-standalone

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
