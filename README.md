# naspotato
This is a collection of config directories for the PVR suite using LinuxServer.io 
container images.
 - radarr
 - jackett
 - plex
 - muximux

The containers (therefore configs) have been updated and run to populate the config
directories with flat files and databases (radarr).  These interelated containers
should work with the docker-compose up command from the start.

Additional Docker bind volume mounts are added to the git repo to allow a simple
git pull from the Docker host to have those directories available to expecting containers.

The transmission-openvpn image is from haugene/transmission-openvpn and feeds:
 - transmission

### TODO
Sonarr and the transmission cleanup image (on home NAS) will need to be added
to the compose file to complete the `naspotato` suite.

Additional testing will be done on a light-weight Synology NAS device in the near future.

### Requirements
 - Docker
 - git
 - disk space :)

## Usage

### docker-compose.yml
Heavy editing has been done to the containers (config) and to the compose file
but user/password for NordVPN has been removed.

Docker Compose must (initially) be called with Shell env vars (or .env file) set for:
 - NORDUSER=<nordVPN username>
 - NORDPASS=<nordVPN password>

`NORDUSER='someuser'; NORDPASS='somepass'; docker-compose up`


