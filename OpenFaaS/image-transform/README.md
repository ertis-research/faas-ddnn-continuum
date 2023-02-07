# image-transform

A function that applies a transformation to a base64 encoded image

> Original instructions: https://docs.openfaas.com/cli/templates/

## Deployment instructions

```sh
# Set the registry location
export DOCKER_REGISTRY=192.168.43.232:5000
# Build the function
faas-cli build -f image-transform.yml
# Deploy the function
faas-cli push -f image-transform.yml
# Set the registry location (from inside the cluster)
export DOCKER_REGISTRY=10.10.32.232:5000
# Deploy the function
faas-cli deploy -f image-transform.yml
```

## Test the function

### Using faas-cli

```sh
$ export OPENFAAS_URL=<host>:<port>
$ printf '{"image": "%s"}' "$(base64 -w0 /lambda/codebrim/images/image_0000001.jpg)" | faas-cli invoke image-transform -m POST
{"response": "..."}
```

### Using cURL

```sh
$ export OPENFAAS_URL=<host>:<port>
$ printf '{"image": "%s"}' "$(base64 -w0 /lambda/codebrim/images/image_0000001.jpg)" | curl http://$OPENFAAS_URL/function/image-transform -X POST -H "Content-Type: application/json" -d@-
{"response": "..."}
```
