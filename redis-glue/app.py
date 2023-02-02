from flask import Flask, request
from redis import Redis

from functools import lru_cache

@lru_cache
def get_redis():
    with open('/etc/redis-glue-config/REDIS_HOSTNAME', 'rt') as hostf, open('/etc/redis-glue-config/REDIS_PORT', 'rt') as portf:
        host = hostf.read()
        port = int(portf.read())
    return Redis(host=host, port=port, db=0)

app = Flask(__name__)

@app.post("/")
def handle():
    payload = request.get_json()
    value = payload['value']
    response = get_redis().set('value', value)
    return {"response": response}

if __name__ == '__main__':
    app.run()
