FROM python:2-alpine3.8

# Update packages and install software
RUN apk add dumb-init && pip install schedule transmissionrpc

# Copy run script(s) to run-dir
ADD opt/ /opt/tor-sched/
WORKDIR /opt/tor-sched/
EXPOSE 8888

# inti the process
CMD ["dumb-init", "python", "torrent-clean.py"]
