FROM python:3.5-alpine

RUN apk -U add ca-certificates && \
    rm /var/cache/apk/*
    
RUN adduser -D -H terribot && \
    chown terribot: /app -R

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

USER terribot

CMD ["python", "terribot.py"]
