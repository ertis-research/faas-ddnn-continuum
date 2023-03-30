from flask import request
from kafka3 import KafkaProducer
from pydantic import parse_obj_as, BaseModel
from functools import lru_cache
from json import load, dumps

class Config(BaseModel):
    producer: dict
    topic: str

    class Config:
        env_nested_delimiter = "_"
        frozen = True
        env_prefix = "FUNNEL_"

@lru_cache(maxsize=1)
def get_config(namespace: str, configmap: str, key: str):
    with open(f"/configs/{namespace}/{configmap}/{key}") as f:
        obj = load(f)
    return parse_obj_as(Config, obj)

# NOTE: lru_cache cant be used as dict's aren't hashable
__kafkaproducer_singleton = None
def get_producer(d: dict):
    global __kafkaproducer_singleton

    if __kafkaproducer_singleton is None:
        __kafkaproducer_singleton = KafkaProducer(**d)
    return __kafkaproducer_singleton

def main():
    payload = request.get_json(force=True)
    function_name = request.headers["X-Fission-Function-Name"]
    namespace = request.headers["X-Fission-Function-Namespace"]
    configmap = "inference"
    config = get_config(namespace, configmap, function_name)
    
    producer = get_producer(config.producer)
    key = payload["key"].encode() if "key" in payload else None
    headers = [(k,v.encode()) for k,v in payload.get("headers", {}).items()]
    producer.send(
        config.topic,
        dumps(payload["value"]).encode(),
        key=key,
        headers=headers
    )
    producer.flush()
    
    return "", 200
