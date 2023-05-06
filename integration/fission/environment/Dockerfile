ARG TENSOR_TAG=2.11.0
FROM tensorflow/tensorflow:${TENSOR_TAG}
RUN apt-get update -y && apt-get install -y python3-dev libev-dev
RUN mkdir app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY server.py .
ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["python3"]
CMD ["server.py"]
