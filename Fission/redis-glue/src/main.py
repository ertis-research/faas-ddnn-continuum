"""
A simple function that updates the `value` key on a Redis database with the 
received payload value
"""
from flask import request
from redis import Redis

def get_redis(namespace: str, configmap: str):
    with open(f'/configs/{namespace}/{configmap}/HOSTNAME', 'rt') as f:
        host = f.read()

    with open(f'/configs/{namespace}/{configmap}/PORT', 'rt') as f:
        port = int(f.read())

    return Redis(
        host=host, 
        port=port, 
        db=0
    )

def main():
    payload = request.get_json()
    value = payload["value"]

    with get_redis('default', 'redis-glue') as r:
        response = r.set('value', value)
    
    return {"response": response}
