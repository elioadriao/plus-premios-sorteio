FROM python:3.8

WORKDIR /home/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV TZ=America/Maceio

ENTRYPOINT ./entrypoint.sh