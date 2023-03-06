from kafka3 import KafkaProducer
from functools import lru_cache
from json import loads, dumps
from os import environ

@lru_cache(maxsize=None)
def get_producer():
    args = loads(environ["FUNNEL_PRODUCER"])
    return KafkaProducer(**args)

@lru_cache(maxsize=None)
def get_producer_options():
    return loads(environ.get("FUNNEL_SEND", default="{}"))

def handle(event, context):
    payload = loads(event.body)
    producer = get_producer()
    kwargs = get_producer_options()

    producer.send(
        environ["FUNNEL_TOPIC"],
        dumps(payload).encode(),
        **kwargs
    ).get(timeout=30)
    
    return {"statusCode": 200}
