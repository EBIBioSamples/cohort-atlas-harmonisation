#!/bin/bash

source ./env.txt

lsof -i tcp:${H_PORT} | grep LISTEN

if [ $? -eq 0 ]; then
  echo "Port ${H_PORT} is already in use. Releasing this port..."
  lsof -ti tcp:${H_PORT} | xargs kill
else
  echo "Port ${H_PORT} is avaiable"
fi
