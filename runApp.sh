#!/bin/bash


echo -n "Enter NordVPN password: "
read -s NORDPASS

export DOCKER_ROOT='/Users/xdxc077/DockerApps'
export NORDUSER='djc@34thplace.net' 
export NORDPASS

docker-compose up
