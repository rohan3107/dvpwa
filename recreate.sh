#!/bin/bash
set -e

docker-compose down --remove-orphans
docker volume ls -qf dangling=true | xargs -r docker volume rm
docker-compose build --memory 500m
