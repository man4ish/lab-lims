#!/bin/sh

docker build -t lims .
docker run --env-file .env -p 8000:8000 lims
