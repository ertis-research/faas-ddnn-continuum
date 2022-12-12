Este documento sirve como guía de instalación de los componentes necesarios en
un cluster de Kubernetes para poder desplegar [KEDA]

Los comandos de la guía están pensados para ser ejecutados en la carpeta actual
(`docs/KEDA`), a no ser que se indique lo contrario

# Requisitos

- Cluster de Kubernetes
- [Helm]

# Instrucciones

> Estos comandos han sido probados en el nodo master (nodo1) del cluster

```sh
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
kubectl create namespace keda
helm install keda kedacore/keda --namespace keda
```

# Desinstalar KEDA

```sh
helm uninstall keda --namespace keda
```

[keda]: https://keda.sh/
[helm]: https://helm.sh/
