# OpenFaaS

```sh
.venv/bin/python scripts/mnist.py bench --brokers=192.168.49.179:32001 --topic=openfaas.inference.edge-input
.venv/bin/python scripts/kafka.py --topics=openfaas.inference.{edge,fog,cloud}-output --brokers=192.168.49.179:32001 --output=ddnn/benchmark/openfaas.json --messages=400
```

# Fission

```sh
.venv/bin/python scripts/mnist.py bench --brokers=192.168.49.179:32001 --topic=fission.inference.edge-input
.venv/bin/python scripts/kafka.py --topics=fission.inference.{edge,fog,cloud}-output --brokers=192.168.49.179:32001 --output=ddnn/benchmark/fission-newdeploy-min1.json --messages=400
```
