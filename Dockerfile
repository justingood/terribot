FROM python:3.5-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

RUN adduser -D -H terribot && \
    chown terribot: /app -R

USER terribot

CMD ["python", "terribot.py"]
