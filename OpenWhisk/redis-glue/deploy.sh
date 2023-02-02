#!/bin/bash

SRC_DIR="$PWD/src"
FUNCTION_ZIP=out/redis-glue.zip

wsk action create redis-glue --kind python:3 --main main out/redis-glue.zip --param-file parameters.json
