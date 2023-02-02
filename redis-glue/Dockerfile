# From https://github.com/ertis-research/kafka-ml/blob/4542ab5dab6e3d03706ac020aedf2bd9ee4bbec0/mlcode_executor/pthexecutor/Dockerfile

# sudo docker build -t 10.10.32.232:5000/redis-glue-flask:0.2.0 .
# sudo docker image push 10.10.32.232:5000/redis-glue-flask:0.2.0

FROM python:3.11
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
# copy project
COPY . /usr/src/app/
EXPOSE 80
CMD gunicorn app:app --bind 0.0.0.0:80 --timeout 0
