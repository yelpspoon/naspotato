#!/bin/bash

# --- 
# Wrapper script to set some user/pw variables for the OpenVPN client.
# Application installation root will also be set from prompts as well
# as running the Docker suit in foreground or background mode.
# NORDUSER & NORDPASS are read in by docker-compose from .env file
# --- 

set -a # all vars will be exported to env

# DEBUG == run in foreground mode
if [ "$1" != "DEBUG" ]; then BACKGROUND='--detach'; else BACKGROUND='';fi

# default app suit root directory
APP_ROOT='/naspotato'

# Read in App base root directory; can use current $(pwd) directory (for testing) or default
echo ""
read -p "Enter Application root directory [enter for ${APP_ROOT} or enter \$(pwd)]: " DOCKER_APP_DIR
if [ "${DOCKER_APP_DIR:0:1}" == "\$" ]; then 
    eval APP_ROOT=${DOCKER_APP_DIR}
elif [ "${DOCKER_APP_DIR}" != "" ]; then 
    APP_ROOT=${DOCKER_APP_DIR}
fi

# /etc/synoinfo.conf
# Set OSTYPE for bind-mount in compose file; run docker compose
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    docker-compose up ${BACKGROUND}
else [[ "$OSTYPE" == "darwin"* ]]
    echo "Using docker-compose.macos.yml"
    docker-compose -f docker-compose.macos.yml up ${BACKGROUND}
fi
