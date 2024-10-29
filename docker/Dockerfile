FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

# Installs the required python packages
RUN pip install -r requirements.txt

# Installs ffmpeg e wget
RUN apt-get update && apt-get install -y ffmpeg unzip wget

COPY src /app/src

# Imposta il PYTHONPATH
ENV PYTHONPATH=/app/src
