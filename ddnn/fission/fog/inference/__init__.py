from flask import request as flask_request
from tensorflow import keras
from functools import lru_cache
from json import load
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, parse_obj_as
from numpy.typing import NDArray
from pathlib import Path
import requests

class ExitSettings(BaseModel):
    url: HttpUrl

class NextSettings(BaseModel):
    url: HttpUrl
    confidence: float

class Config(BaseModel):
    model: str
    exit: ExitSettings
    next: Optional[NextSettings]

    class Config:
        env_nested_delimiter = "_"
        frozen = True

@lru_cache(maxsize=1)
def get_config(namespace: str, configmap: str, key: str):
    with open(f"/configs/{namespace}/{configmap}/{key}") as f:
        obj = load(f)
    return parse_obj_as(Config, obj)

@lru_cache(maxsize=1)
def model(model: str):
    file = Path(__file__).resolve().parent.joinpath(model)
    return keras.models.load_model(file)

def main():
    payload = flask_request.get_json(force=True)
    function_name = flask_request.headers["X-Fission-Function-Name"]
    namespace = flask_request.headers["X-Fission-Function-Namespace"]
    configmap = "inference"
    config = get_config(namespace, configmap, function_name)
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
    
    return {"status": response.status_code, "body": response.text}, response.status_code

