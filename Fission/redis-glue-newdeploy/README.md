# redis-glue-newdeploy

A simple function that updates the `value` key on a Redis database with the
received payload value

- Executor kind: `newdeploy`
- Minscale: 0

> Original instructions: https://fission.io/docs/usage/spec/

## Deployment instructions

```sh
# Load the function required config map and secrets
kubectl apply -f ../config.yml
# Lauch the function on fission
fission spec apply --wait
```

## Test the function

### Using fission's CLI

```sh
$ fission fn test --name redis-glue-newdeploy --method POST -b '{"value": 10}' -H 'Content-Type: application/json'
{"response": true}
```

### Using cURL

```sh
$ export FISSION_HOST=<host>
$ export FISSION_PORT=<port>
$ curl http://$FISSION_HOST:$FISSION_PORT/redis-glue-newdeploy -X POST -H "Content-Type: application/json" -d '{"value": 10}'
{"response": true}
```
