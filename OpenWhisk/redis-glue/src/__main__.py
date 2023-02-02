"""
A simple function that updates the `value` key on a Redis database with the 
received payload value
"""
from redis import Redis
from typing import Any

def main(payload: dict[str, Any]):
    value = payload["value"]
    redis_host= payload["REDIS_HOSTNAME"]
    redis_port= int(payload["REDIS_PORT"])

    with Redis(host=redis_host, port=redis_port) as r:
        response = r.set('value', value)
    
    return {"response": response}
