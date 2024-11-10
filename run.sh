#!/bin/bash

CURRENT_DIR=$(pwd)

cd docker

BUILD_OPTION="up -d" # Comando predefinito senza build
if [[ $1 == "-b" ]]; then
    BUILD_OPTION="up --build -d" # Aggiungi l'opzione --build
fi


docker-compose $BUILD_OPTION

cd "$CURRENT_DIR"
