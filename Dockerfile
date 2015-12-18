FROM python:3.5

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

RUN useradd -ms /bin/bash terribot && \
    chown terribot: /app -R

USER terribot

ENTRYPOINT ["python", "terribot.py"]
