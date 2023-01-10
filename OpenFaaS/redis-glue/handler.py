"""
A simple function that updates the `value` key on a Redis database with the 
received payload value
"""
from redis import Redis
from json import loads
from os import environ

def get_redis():
    host = environ['REDIS_HOSTNAME']
    port = int(environ['REDIS_PORT'])
    
    return Redis(
        host=host, 
        port=port, 
        db=0
    )

def handle(event, context):
    payload = loads(event.body)
    value = payload["value"]

    with get_redis() as r:
        response = r.set('value', value)
    
    return {
        "statusCode": 200,
        "body": {"response": response},
    }
