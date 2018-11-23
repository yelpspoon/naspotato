# naspotato

This is a collection of config directories for the PVR suite:
The images are from LinuxServer.io except Transmission (haugene/transmission-openvpn)
 - radarr (movie PVR)
 - bazarr (subtitle downloader)
 - jackett (torrent proxy)
 - plex server (media server)
 - muximux (Web Panel for web apps)
 - transmission-openvpn (torrent download client with NordVPN)

The containers (and therefore configs) have been run to populate config/
with flat files and databases (radarr, jackett).  These interelated containers
should work with the docker-compose up command from the start.

Docker bind volume mount directories are added to the git repo to allow a simple
git pull from the Docker host to have those directories available to expecting containers.


### Requirements
 - Docker
 - git
 - disk space :)

## Usage
The app suite would work best if installed in / but not required (update DOCKER_ROOT if 
another location is used -- see below).

 - cd /  # or other dir
 - `git pull https://github.com/yelpspoon/naspotato.git`
 - use one of the two methods below to bring up the app suite

### docker-compose.yml
Heavy editing has been done to the containers (config) and to the compose file
but user/password for NordVPN has been removed.

Docker Compose must (initially) be called with Shell env vars (or .env file) set for:
 - NORDUSER=<nordVPN username>
 - NORDPASS=<nordVPN password>
 - DOCKER_ROOT=<path to some app root>

`export DOCKER_ROOT='/naspotato'; export NORDUSER='someuser'; export NORDPASS='somepass'; docker-compose up`

### runApp.sh
Or you can use runApp.sh which will prompt for NORDPASS.
Edit for username and/or app root directory (which if pulled from git, will be `naspotato`).
Script will prompt for DOCKER_ROOT or use default.

#### Post first-run steps
It may be necessary to clean up the Radarr and Plex movie database as both `downloads` and `movies` in git will not have any movies.

### MacOS concerns
I have had trouble bind-mounting /etc/localtime; this is fairly well-known issue with the lastest 2-3 version of Docker.
I simply remove that mount when running on MacOS and live with the time being UTC in my containers.  MacOS is usually just POC.
The helper script `runApp.sh` will determine OS (Mac or Linux) at run-time and execute accordingly

### TODO
 - Sonarr and the torrent cleanup container (on home NAS) will need to be added to the compose file to complete the `naspotato` suite.
 - Add more indexers to Jackett.
 - Additional testing will be done on a light-weight Synology NAS device in the near future.
