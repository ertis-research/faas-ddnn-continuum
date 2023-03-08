from kafka3 import KafkaProducer
from pydantic import BaseSettings
from functools import lru_cache
from json import loads, dumps

class Config(BaseSettings):
    producer: dict
    topic: str

    class Config:
        env_nested_delimiter = "_"
        frozen = True
        env_prefix = "FUNNEL_"

@lru_cache(maxsize=None)
def get_config():
    return Config()

@lru_cache(maxsize=None)
def get_producer():
    config = get_config()
    return KafkaProducer(**config.producer)

def handle(event, context):
    payload: dict = loads(event.body)
    producer = get_producer()
    config = get_config()
    key = payload["key"].encode() if "key" in payload else None
    headers = [(k,v.encode()) for k,v in payload.get("headers", {}).items()]
    producer.send(
        config.topic,
        dumps(payload["value"]).encode(),
        key=key,
        headers=headers
    )
    producer.flush()
    
    return {"statusCode": 200}
