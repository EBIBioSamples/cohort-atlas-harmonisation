#!/bin/bash

source ./env

docker build -t cohort-atlas-harmonisation .

lsof -i :${FLASK_PORT}

docker run -d -p ${EXT_PORT}:${FLASK_PORT} -v $(pwd)/shared:/app/shared --name coh-atlas cohort-atlas-harmonisation
