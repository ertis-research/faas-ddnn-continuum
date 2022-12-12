Este documento sirve como guía de instalación de los componentes necesarios en
un cluster de Kubernetes para poder desplegar un [ingress controller]

Los comandos de la guía están pensados para ser ejecutados en la carpeta actual
(`docs/Ingress`), a no ser que se indique lo contrario

# Nginx

## Instalar

- https://kubernetes.github.io/ingress-nginx/deploy/

```sh
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

## Dar de baja el servicio

```sh
helm uninstall ingess-nginx -n fission
```

[ingress controller]:
  https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers
