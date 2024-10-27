FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Scarica e estrai il modello Vosk in un unico comando RUN
ARG MODEL_URL
RUN apt-get update && apt-get install -y ffmpeg unzip wget  && \
    wget -O vosk-model.zip ${MODEL_URL} && \
    unzip vosk-model.zip -d /app/vosk-model

COPY src /app/src

# Imposta il PYTHONPATH
ENV PYTHONPATH=/app/src
