from typer import Option, Typer
from kafka3 import KafkaProducer

from functools import lru_cache
from typing import List
from json import dumps
from uuid import uuid4
from time import time, sleep

from lib import NumpyEncoder


@lru_cache(maxsize=None)
def mnist():
    from tensorflow import keras
    return keras.datasets.mnist.load_data()

def payload_raw(start:int, end:int):
    (x_train, y_train), (test, y_test) = mnist()
    value = test[start:end]
    return value[0].tobytes()

def payload(start: int, end: int):    
    (x_train, y_train), (test, y_test) = mnist()
    value = test[start:end]
    return dumps(value, cls=NumpyEncoder).encode()

app = Typer()

@app.command()
def json(blocksize: int = 1, offset: int = 0):
    p = payload(offset, offset + blocksize)
    print(p)

@app.command()
def kafka(topic: str, brokers: List[str], batch_size: int = 1, offset: int = 0, messages: int = 5, batch_sleep: float = 0, payload_fn=payload):
    producer = KafkaProducer(bootstrap_servers=brokers)

    for i in range(messages):
        p = payload_fn(offset + i * batch_size, offset + (1 + i * batch_size))
        producer.send(topic, p, key=str(uuid4()).encode(), headers=[("X-INFERENCE-TS", str(time()).encode())])
        producer.flush()
        sleep(batch_sleep)
    
    producer.close()

@app.command()
def bench(
    topic: str = Option(...),
    brokers: List[str] = Option(...),
    raw: bool = False,
):
    print(f'Bench startup time: {time()}')
    total_messages = 0

    for stage in range(1, 5):
        messages = 100
        batch_sleep = 1 / stage
        total_messages += messages

        payload_fn = payload_raw if raw else payload
        kafka(topic, brokers,messages=messages, batch_sleep=batch_sleep,payload_fn=payload_fn)
        print({
            'stage': stage,
            'messages': messages,
            'batch_sleep': batch_sleep,
            'total_messages': total_messages
        })

if __name__ == '__main__':
    app()
