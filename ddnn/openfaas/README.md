# Requisites

- **edge**: Cluster de RPI
- **fog**: Pepino
- **cloud**: Cluster de k8s de ERTIS

```sh
# Load the environment file
export $(cat ../.env | xargs)
# Deploy edge. Note: must be run from an aarch64 machine
DOCKER_PREFIX=$DDNN_CLOUD_IP:30501 faas up -f edge.yml
# Deploy fog
DOCKER_PREFIX=$DDNN_CLOUD_IP:30501 faas up -f fog.yml
# Deploy cloud
DOCKER_PREFIX=$DDNN_CLOUD_IP:30501 faas build -f cloud.yml
DOCKER_PREFIX=$DDNN_CLOUD_IP:30501 faas push -f cloud.yml
DOCKER_PREFIX=10.10.32.10:30501 faas deploy -f cloud.yml
```
