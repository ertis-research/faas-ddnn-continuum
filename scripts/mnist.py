from typer import Typer
from kafka3 import KafkaProducer

from functools import lru_cache
from typing import List

@lru_cache(maxsize=None)
def mnist():
    from tensorflow import keras
    return keras.datasets.mnist.load_data()

def payload(start: int, end: int):
    from lib import NumpyEncoder
    from json import dumps
    
    (x_train, y_train), (x_test, y_test) = mnist()
    value = x_test[start:end]
    return dumps({"value": value}, cls=NumpyEncoder)

app = Typer()

@app.command()
def json(blocksize: int = 1, offset: int = 0):
    p = payload(offset, offset + blocksize)
    print(p)

@app.command()
def kafka(topic: str, brokers: List[str], blocksize: int = 1, offset: int = 0, messages: int = 5):
    producer = KafkaProducer(bootstrap_servers=brokers)

    for i in range(messages):
        p = payload(offset + i * blocksize, offset + (1 + i * blocksize))
        producer.send(topic, p.encode())

    producer.flush()
    
if __name__ == '__main__':
    app()
