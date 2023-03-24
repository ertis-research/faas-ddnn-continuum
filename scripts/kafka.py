from kafka3 import KafkaConsumer
from typer import Option, Typer
from typing import List
from pathlib import Path
from json import dump

app = Typer()

@app.command()
def download(
    topics: List[str] = Option(...),
    brokers: List[str] = Option(...),
    output: Path = Option(...),
    messages: int = Option(...),
):
    # Await responses
    consumer = KafkaConsumer(bootstrap_servers=brokers, auto_offset_reset='earliest')
    consumer.subscribe(topics)

    with open(output, 'a') as f:
        for (indx, msg) in enumerate(consumer):
            print(msg.key)
            payload = {
                'topic': msg.topic,
                'partition': msg.partition,
                'offset': msg.offset,
                'timestamp': msg.timestamp,
                'key': msg.key.decode(),
                'first_timestamp': [(k,v.decode()) for k,v in msg.headers],
                # Value is meaningless and takes too much disk space
                # 'value': msg.value.decode()
            }
            dump(payload, f)
            f.write('\n')
            f.flush()

            if indx == messages - 1:
                break

if __name__ == '__main__':
    app()
