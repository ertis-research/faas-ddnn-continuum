# K6 Load testing

Scripts and Kubernetes resources ready to test other services

## Prerequisites

Prepare the `/lambda` directory on the current node

```sh
sudo mkdir -p /lambda/k6/out
# All users can read and write
sudo chmod -R a+rw /lambda
cp -r . /lambda/k6
```

## fission-default-1h-redis-glue

For [`Fission/redis-glue`](../Fission/redis-glue)

- Dataset contains 96 elements
- Sends request every hour
- Takes 4 days to complete

```sh
kubectl apply -f /lambda/k6/fission-default-1h-redis-glue.yml
```

### Get results

- CSV: `/lambda/k6/out/results-fission-default-1h-redis-glue.csv`
- Logs: `kubectl logs k6-load-deployment-fission-default-1h-redis-glue`

### Cleanup

```sh
kubectl delete pod k6-load-deployment-fission-default-1h-redis-glue
```
