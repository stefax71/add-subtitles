#!/bin/bash

# Controlla se ffmpeg è installato
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg non trovato. Per favore installalo prima di eseguire questo script."
    exit 1
fi

# Controlla che siano stati forniti tutti gli argomenti necessari
if [ "$#" -ne 3 ]; then
    echo "Utilizzo: $0 <video.mp4> <subtitles.srt> <output.mp4>"
    exit 1
fi

# Input video, sottotitoli e output
VIDEO=$1
SUBTITLES=$2
OUTPUT=$3

# Comando ffmpeg per aggiungere i sottotitoli
ffmpeg -i "$VIDEO" -vf subtitles="$SUBTITLES" -c:a copy "$OUTPUT"

# Controlla se il comando ha avuto successo
if [ $? -eq 0 ]; then
    echo "Sottotitoli aggiunti con successo: $OUTPUT"
else
    echo "Errore durante l'aggiunta dei sottotitoli."
    exit 1
fi
