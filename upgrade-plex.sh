#!/bin/bash

sudo docker-compose pull plex

#sudo docker-compose up --force-recreate --build -d plex
sudo docker-compose up -d --force-recreate --no-deps plex
sudo docker image prune -f
