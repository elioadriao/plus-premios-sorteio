FROM python:3.8

WORKDIR /home/app

RUN apt-get update && pip install psycopg2-binary

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN rm /bin/sh && ln -s /bin/bash /bin/sh