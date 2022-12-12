# HTTP

- https://fission.io/docs/usage/ingress/

<!-- TODO https://github.com/fission/fission/issues/2650 -->

# Kafka

- https://fission.io/docs/usage/triggers/message-queue-trigger-kind-keda/kafka/
- https://keda.sh/docs/1.4/scalers/apache-kafka/

```sh
# Topics de Kafka
export TOPIC_IN=''
export TOPIC_OUT=''
export TOPIC_ERROR=''
# Nombre del trigger
export TRIGGER_NAME=''
# Nombre de la función
export FUNCTION_NAME=''
# bootstrap servers de Kafka, separados por coma
# Ej: 192.168.43.232:9095,192.168.43.233:9096
export KAFKA_SERVERS=''

fission mqt create \
  --mqtkind keda \
  --mqtype kafka \
  --maxretries 3 \
  --cooldownperiod=30 \
  --pollinginterval=5 \
  --name "$TRIGGER_NAME" \
  --function "$FUNCTION_NAME" \
  --topic "$TOPIC_IN" \
  --resptopic "$TOPIC_OUT" \
  --errortopic "$TOPIC_ERROR" \
  --metadata "bootstrapServers=$KAFKA_SERVERS" \
  --metadata "consumerGroup=$FUNCTION_NAME" \
  --metadata "topic=$TOPIC_IN"
```
