```sh
curl http://node1:30092/redis-glue \
 -X POST \
 -H "Content-Type: application/json" \
 -d '{"value": 10}'
```

```sh
fission fn test --name redis-glue --method POST -b '{"value": 10}' -H 'Content-Type: application/json'
```