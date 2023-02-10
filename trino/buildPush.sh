#!/bin/bash
docker build -t guestros/ranger:latest --file Dockerfile.rangeradmin .
docker build -t guestros/trino:latest --file Dockerfile.trino .

docker push guestros/ranger:latest
docker push guestros/trino:latest