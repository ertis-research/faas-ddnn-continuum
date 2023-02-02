#!/bin/bash
set -ex

DOCKER_IMAGE=openwhisk/python3action
SRC_DIR="$PWD/src"
FUNCTION_ZIP=out/redis-glue.zip

rm -fr out src/virtualenv
docker run --rm -v "$SRC_DIR:/tmp" "$DOCKER_IMAGE" bash \
  -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"

mkdir out
zip -r "$FUNCTION_ZIP" src/*
