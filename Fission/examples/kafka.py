from flask import request

# Instrucciones de despliegue

# $ fission environment create --name python --image fission/python-env
# $ fission function create --name kafka-py --env python --code kafka.py
# $ fission function test --name kafka-py
# 
# $ export TOPICIN=fission-input
# $ export TOPICOUT=fission-output
# $ export TOPICERROR=fission-error
# $ fission mqt create --name kafka-py-conn --function kafka-py --mqtype kafka --mqtkind keda --topic "$TOPICIN" --resptopic "$TOPICOUT" --errortopic "$TOPICERROR" --maxretries 3 --metadata bootstrapServers=192.168.43.232:9095 --metadata consumerGroup=kafka-py --metadata "topic=$TOPICIN"  --cooldownperiod=30 --pollinginterval=5 


def main():
    return request.get_data()