FROM python3.11

RUN pip3 install -r requirements.txt

COPY src /app

WORKDIR /app

ENTRYPOINT main.py
