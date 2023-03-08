from tensorflow import keras
from json import loads
from functools import lru_cache
from typing import Optional, List
from pydantic import BaseSettings, BaseModel, HttpUrl
from numpy.typing import NDArray
import requests

class ExitSettings(BaseModel):
    url: HttpUrl

class NextSettings(BaseModel):
    url: HttpUrl
    confidence: float

class Config(BaseSettings):
    model: str
    exit: ExitSettings
    next: Optional[NextSettings]

    class Config:
        env_nested_delimiter = "_"
        frozen = True

@lru_cache(maxsize=None)
def get_config():
    return Config()

@lru_cache(maxsize=1)
def model(model: str): 
    return keras.models.load_model(model)

def handle(event, context):
    config = get_config()
    payload = loads(event.body)
    # raise ValueError(payload)
    value = payload["value"]
    m = model(config.model)
    # raise ValueError(value)
    prediction: NDArray | List[NDArray] = m.predict(value)

    # if middle layer, distributed ML
    if (config.next is not None) and (config.next.confidence is not None):
        prediction_to_upper, prediction_exit = prediction

        if prediction_exit.max() >= config.next.confidence:    
            request = config.exit
            request_payload = prediction_exit
        else:
            request = config.next
            request_payload = prediction_to_upper
    else:
        request = config.exit
        request_payload = prediction

    payload["value"] = request_payload.tolist()
    response = requests.post(request.url, json=payload)
    
    return {
        "statusCode": response.status_code,
        "body": {
            "status": response.status_code,
            "body": response.text
        },
    }
