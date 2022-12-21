"""
A simple function that updates the `value` key on a Redis database with the 
received payload value

Environment:
    FUNCTION_REDIS_HOSTNAME (str)
    FUNCTION_REDIS_PORT (int)
"""
from os import environ
from json import loads
import redis

# Set environment variables
host = environ['FUNCTION_REDIS_HOSTNAME']
port = int(environ['FUNCTION_REDIS_PORT'])

r = redis.Redis(
    host=host, 
    port=port, 
    db=0
)

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    payload = loads(req)
    value = payload["value"]
    r.set('value', value)
    return req
