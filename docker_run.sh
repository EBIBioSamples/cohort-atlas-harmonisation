#!/bin/bash

source ./env.txt

docker build -t cohort-atlas-harmonisation .

lsof -i :${H_PORT}

docker run -d -p ${EXT_PORT}:${H_PORT} --name coh-atlas cohort-atlas-harmonisation
