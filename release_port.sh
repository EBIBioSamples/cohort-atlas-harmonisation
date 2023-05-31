#!/bin/bash

source ./env.txt

lsof -i tcp:${EXT_PORT} | grep LISTEN

if [ $? -eq 0 ]; then
  echo "Port ${EXT_PORT} is already in use. Releasing this port..."
  lsof -ti tcp:${EXT_PORT} | xargs kill
else
  echo "Port ${EXT_PORT} is avaiable"
fi
