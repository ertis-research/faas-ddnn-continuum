from flask import Flask, request
from tensorflow import keras
from os import environ, path
from functools import lru_cache
import numpy as np
from io import BytesIO

SENTRY_DSN = environ.get('SENTRY_DSN', None)
SENTRY_RELEASE = environ.get('SENTRY_RELEASE', None)
USERFUNCVOL = environ.get("USERFUNCVOL", "/userfunc")
RUNTIME_PORT = int(environ.get("RUNTIME_PORT", "8888"))

app = Flask(__name__)

user_model = None

@lru_cache(maxsize=1)
def load_keras_model(route: str):
    return keras.models.load_model(route)

@app.route("/v2/specialize", methods=["POST"])
def specialize2():
    global user_model
    payload = request.get_json()
    user_model = path.join(payload["filepath"], 'model.h5')
    # Preload
    model = load_keras_model(user_model)
    model.summary()
    return ""

@app.route("/healthz", methods=["GET"])
def health():
    return "", 200

@app.route("/", methods=['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE'])
def inference():
    model = load_keras_model(user_model)
    input_buffer = BytesIO(request.get_data())
    input_data = np.load(input_buffer)
    prediction = model.predict(input_data)
    prediction_value = prediction.tolist()[0]
    return {"values": prediction_value}, 200
    
if __name__ == '__main__':
    from bjoern import run
    run(app, '0.0.0.0', RUNTIME_PORT, reuse_port=True)
