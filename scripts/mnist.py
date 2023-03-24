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

def payload(start: int, end: int):    
    (x_train, y_train), (test, y_test) = mnist()
    value = test[start:end]
    return dumps(value, cls=NumpyEncoder)

app = Typer()

@app.command()
def json(blocksize: int = 1, offset: int = 0):
    p = payload(offset, offset + blocksize)
    print(p)

@app.command()
def kafka(topic: str, brokers: List[str], batch_size: int = 1, offset: int = 0, messages: int = 5, batch_sleep: float = 0):
    producer = KafkaProducer(bootstrap_servers=brokers)

    for i in range(messages):
        p = payload(offset + i * batch_size, offset + (1 + i * batch_size))
        producer.send(topic, p.encode(), key=str(uuid4()).encode(), headers=[("X-INFERENCE-TS", str(time()).encode())])
        producer.flush()
        sleep(batch_sleep)
    
    producer.close()

@app.command()
def bench(
    topic: str = Option(...),
    brokers: List[str] = Option(...),
):
    print(f'Bench startup time: {time()}')
    total_messages = 0

    for stage in range(1, 5):
        messages = 100
        batch_sleep = 1 / stage
        total_messages += messages

        kafka(topic, brokers,messages=messages, batch_sleep=batch_sleep)
        print({
            'stage': stage,
            'messages': messages,
            'batch_sleep': batch_sleep,
            'total_messages': total_messages
        })

if __name__ == '__main__':
    app()
