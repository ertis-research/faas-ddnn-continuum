# OpenFaaS

## 1 IoT

```sh
.venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=openfaas.inference.fog-input
.venv/bin/python scripts/kafka.py --topics=openfaas.inference.{fog,cloud}-output --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/openfaas.json --messages=400
```

## 3 IoT

```sh
for i in {1..3}
do
  .venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=openfaas.inference.fog-input &
done
wait

.venv/bin/python scripts/kafka.py --topics=openfaas.inference.{fog,cloud}-output --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/openfaas3.json --messages=1200
```

- Stage 2: 2 replicas inference. Then 3
- Stage 3: 4 replicas
- Stage 4: 5 replicas

## 5 IoT

```sh
for i in {1..5}
do
  .venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=openfaas.inference.fog-input &
done
wait

.venv/bin/python scripts/kafka.py --topics=openfaas.inference.{fog,cloud}-output --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/openfaas5.json --messages=2000
```

- Stage 2: 2 replicas a 3.
- Stage 3: 4 replicas
- Stage 5: 5 replicas

## 10 IoT

```sh
for i in {1..10}
do
  .venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=openfaas.inference.fog-input &
done
wait

.venv/bin/python scripts/kafka.py --topics=openfaas.inference.{fog,cloud}-output --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/openfaas10.json --messages=4000
```

- Stage 1: 3 fog, despues a 4, despues 5
- Stage 4: Funnel fog output 2 y funnel cloud input 2

# Fission

## 1 IoT

```sh
.venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=fission.inference.fog-input
.venv/bin/python scripts/kafka.py --topics=fission.inference.{fog,cloud}-output --brokers=192.168.48.206:32001 --output=ddnn/benchmark/fission-newdeploy-min1.json --messages=400
```

## 3 IoT

```sh
for i in {1..3}
do
  .venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=fission.inference.fog-input &
done
wait

.venv/bin/python scripts/kafka.py --topics=fission.inference.{fog,cloud}-output --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/fission3-newdeploy-min1.json --messages=1200
```

- Stage 3: 2 fog replicas

## 5 IoT

```sh
for i in {1..5}
do
  .venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=fission.inference.fog-input &
done
wait

.venv/bin/python scripts/kafka.py --topics=fission.inference.{fog,cloud}-output --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/fission5-newdeploy-min1.json --messages=2000
```

- Stage 2: 2 replicas for inference on fog

## 10 IoT devices

```sh
for i in {1..10}
do
  .venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=fission.inference.fog-input &
done
wait

.venv/bin/python scripts/kafka.py --topics=fission.inference.{fog,cloud}-output --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/fission10-newdeploy-min1.json --messages=4000
```

- Stage 1: 2 replicas for inference on fog

# Kafkaml

## 1 IoT

```sh
.venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=kafkaml.inference.fog-input --raw
.venv/bin/python scripts/kafka.py --topics=kafkaml.inference.{fog-output,output-cloud} --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/kafkaml.json --messages=400
```

- Benchmark start: `1682071612.1225128`

## 3 IoT

```sh
for i in {1..3}
do
  .venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=kafkaml.inference.fog-input --raw &
done
wait

.venv/bin/python scripts/kafka.py --topics=kafkaml.inference.{fog-output,output-cloud} --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/kafkaml3.json --messages=1200
```

- Benchmark start: `1682072010.837343`

## 5 IoT

```sh
for i in {1..5}
do
  .venv/bin/python scripts/mnist.py bench --brokers=192.168.48.206:32001 --topic=kafkaml.inference.fog-input --raw &
done
wait

.venv/bin/python scripts/kafka.py --topics=kafkaml.inference.{fog-output,output-cloud} --brokers=192.168.48.206:32001 --output=ddnn2/benchmark/kafkaml5.json --messages=2000
```

- Benchmark start: `1682072307.7277372`
