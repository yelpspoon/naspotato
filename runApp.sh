#!/bin/bash

set -a

read -sp 'Enter NordVPN password: ' NORDPASS

DOCKER_ROOT='/naspotato'
NORDUSER='djc@34thplace.net' 

# Read in App base root directory; can use current $(pwd) directory (for testing) or default
echo ""
read -p "Enter Application root directory [enter for ${DOCKER_ROOT} or enter \$(pwd)]: " DOCKER_APP_DIR

if [ "${DOCKER_APP_DIR:0:1}" == "\$" ]; then 
    eval DOCKER_ROOT=${DOCKER_APP_DIR}
elif [ "${DOCKER_APP_DIR}" != "" ]; then 
    DOCKER_ROOT=${DOCKER_APP_DIR}
fi

# Set OSTYPE for bind-mount
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    docker-compose up
else [[ "$OSTYPE" == "darwin"* ]]
    echo "Using docker-compose.macos.yml"
    docker-compose -f docker-compose.macos.yml up
fi
