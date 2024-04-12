FROM python:3.12

COPY requirements.txt /

RUN pip3 install -r requirements.txt

COPY src /app

COPY Samples /Samples

WORKDIR /app

ENTRYPOINT ./main.py
