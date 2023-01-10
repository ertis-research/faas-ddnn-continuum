# redis-glue

A simple function that updates the `value` key on a Redis database with the
received payload value

> Original instructions: https://docs.openfaas.com/cli/templates/

## Deployment instructions

```sh
# Set the registry location
export DOCKER_REGISTRY=192.168.43.232:5000
# Build the function
faas-cli build -f redis-glue.yml
# Deploy the function
faas-cli push -f redis-glue.yml
# Set the registry location (from inside the cluster)
export DOCKER_REGISTRY=10.10.32.232:5000
# Deploy the function
faas-cli deploy -f redis-glue.yml
```

## Test the function

### Using faas-cli

```sh
$ export OPENFAAS_URL=<host>:<port>
$ echo '{"value": 10}' | faas-cli invoke redis-glue -m POST
{"response": true}
```

### Using cURL

```sh
$ export OPENFAAS_URL=<host>:<port>
$ curl http://$OPENFAAS_URL/function/redis-glue -X POST -H "Content-Type: application/json" -d '{"value": 10}'
{"response": true}
```
