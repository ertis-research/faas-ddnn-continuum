from flask import Flask, request
from os import environ, path
from functools import lru_cache
from pydantic import parse_file_as, BaseModel
from requests import get
from tempfile import NamedTemporaryFile
from urllib.parse import urljoin

# SENTRY_DSN = environ.get('SENTRY_DSN', None)
# SENTRY_RELEASE = environ.get('SENTRY_RELEASE', None)
# USERFUNCVOL = environ.get("USERFUNCVOL", "/userfunc")
RUNTIME_PORT = int(environ.get("RUNTIME_PORT", "8888"))

app = Flask(__name__)

user_config = None

class UserConfig(BaseModel):
    backend: str
    model: str
    class Config:
        frozen = True

@lru_cache(maxsize=1)
def load_keras_model(config: UserConfig):
    from tensorflow import keras
    response = get(urljoin(config.backend, f"/results/model/{config.model}"))
    response.raise_for_status()
    
    with NamedTemporaryFile('wb') as f:
        f.write(response.content)
        f.flush()
        model = keras.models.load_model(f.name)
    
    return model

@app.route("/v2/specialize", methods=["POST"])
def specialize2():
    global user_config
    payload = request.get_json()
    filepath = payload["filepath"]
    function_name = payload["functionName"]

    config_file = path.join(filepath, function_name)
    user_config = parse_file_as(UserConfig, config_file)

    model = load_keras_model(user_config)
    model.summary()
    return ""

@app.route("/", methods=['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE'])
def inference():
    model = load_keras_model(user_config)
    input_data = request.get_json(force=True)
    prediction = model.predict(input_data)
    prediction_value = prediction.tolist()[0]
    return {"values": prediction_value}, 200

@app.route("/healthz", methods=["GET"])
def health():
    return "", 200
    
if __name__ == '__main__':
    from bjoern import run
    run(app, '0.0.0.0', RUNTIME_PORT, reuse_port=True)
