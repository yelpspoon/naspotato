#!/bin/bash

sudo docker-compose pull sonarr
#sudo docker-compose pull bazarr
sudo docker-compose pull jackett
sudo docker-compose pull transmission
sudo docker-compose pull plex
sudo docker-compose pull muximux

sudo docker-compose down
sudo docker-compose up --force-recreate --build -d 

sudo docker image prune -f
