# naspotato

`naspotato` is a suite of Docker containers to run PVRs to download TV shows and movies using
`transmission` with a built in openvpn client to 'run silent'.
`muximux` is used to aggregate all the App web front-ends in one browser tab (<nas/localhost>:8080).
`Plex` is used as DNLA server since most TVs/devices now have a Plex client to view media content.


The images are from LinuxServer.io except Transmission (haugene/transmission-openvpn)
 - sonarr (TV PVR)
 - radarr (movie PVR)
 - bazarr (subtitle downloader)
 - jackett (torrent proxy)
 - plex server (media server)
 - muximux (Web Panel for web apps)
 - transmission-openvpn (torrent download client with NordVPN)
 - tran-cleaner (Custome Py script and image to remove old torrents)

Containers have been run to populate the `/config` directories of each of the Apps
that _need_ manual front-end configuration (sonarr, radarr, jackett).  The `/config` directories
contain persistent data that will survive reruns and git pulls ( along with the actual Media Volumes referred to by the bind-mounts).

The goal is to clone the repo, make minimal mods (see below), issue `docker-compose up` and be running.

#### Mods Overview
 - Docker bind volume mount directories (docker-compose.yml)
 - VPN user / pass info (.env file)
 - UID & GID for access to local volumes
 - muximux setup for the Apps you wish to see in the panel (muximux container)
 - Review port mappings of existing apps (or NAS DNLA [Plex] or Bonjour port usage) [Synology NAS]

The git repo has a `data-directories` folder for use with a generic (new) `up and run` situation.
Modifications of the docker-compose.yml bind mounts (last section in the file) will be needed
for NAS/local directories of existing media directories.


### System Requirements
 - Docker
 - git
 - disk space :)

## Usage
The app suite is expecting to run in `naspotato/`. The value of APP_ROOT either in `.env` or exported via shell should be updated if `naspotato/` is not at root filesystem level so that Docker bind-mounts are Absolute.

#### Example Steps
 - cd /  # or other installation directory
 - `git pull https://github.com/yelpspoon/naspotato.git`
 - use one of the two methods below to bring up the app suite

### MANUAL docker-compose docker-compose.yml up
This would be run for permanent App suite starts.

Docker Compose must be called with Shell env vars (or .env file) set for:
 - NORDUSER=\<nordVPN username>
 - NORDPASS=\<nordVPN password>
 - APP_ROOT=\<path to some app root>
 - VOLUME_ROOT=\<path to non-git repo defined volume location>
 - UID=1026
 - GID=101

`export APP_ROOT='/naspotato'; export NORDUSER='someuser'; export... ; docker-compose up [-d]`

Better, create a `.env` file which will be consumed by `docker-compose up`

```
NORDUSER=username
NORDPASS=password
UID=101
GID=101
APP_ROOT=/volume2/docker/naspotato
VOLUME_ROOT=/volume1/NasMedia
```

### runApp.sh Helper Script
This script is helpful determining various ENV Var settings and provides usage for Mac POCs.

`runApp.sh [DEBUG]` 
 - DEBUG will not run detached to show logs in stdout

The script will prompt for APP_ROOT or use default `/naspotato`
Cloning from git will mean you are running from `/path/to/naspotato` which should assigned to APP_ROOT
You can pass in `$(pwd)` to the script which will construct an 'absolute' path for APP_ROOT.
VOLUME_ROOT, if different than `/naspotato/data-directories` must be set in script or `.env`.

#### Post first-run steps
It may be necessary to clean up the Radarr and Plex movie database as both `downloads` and `movies`. 
There may be residual data in the app metadata databases which may not match (any) media in the media directories of a new installation.

### MacOS concerns
I have had trouble bind-mounting /etc/localtime; this is fairly well-known issue with the last 2-3 versions of Docker.
I simply remove that mount when running on MacOS and live with the time being UTC in my containers.  MacOS is usually just POC.
The helper script `runApp.sh` will determine OS (Mac or Linux) at run-time and execute accordingly

### Notes (Synology NAS 918+ DSM 6.2.1)
 - My personal use required heavy mods of the bind mounts to suit my existing media dirs (TV, Movies, Video).
 - Plex had issues with ports 1900 (media server or UPnP ports) and 5353 (Bonjour) on DSM Synology.
   - Disable 1900 via Control Panel -> File Services -> Advanced -> SSDP (uncheck)
   - Plex 5353 was not published (dunno the side effects, if any).
 - .gitignore _should_ eliminate pushing Plex metadata to git; this can be GB in size; caveat emtor.
 - Additional testing will be done on a light-weight Synology NAS device in the near future.
 - Test Plex client on the network to see if it can "discover" the naspotato suite.
