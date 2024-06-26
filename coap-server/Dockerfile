# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

# 2024-06-05 Wireshark installation: https://www.youtube.com/watch?v=k23qhS8vPBQ 

FROM ubuntu:20.04 as base

#MAINTAINER Gianluca Carbone <gianlucarbone96@gmail.com>
USER root
RUN DEBIAN_FRONTEND=noninteractive
RUN export DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y sudo \ 
    && apt-get install -y python3 python3-venv \
    && apt-get install -y tshark
    #&& apt-get install -y iproute2 \
    
RUN groupadd wireshark

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
# Debug mode with Asyncio - https://docs.python.org/3/library/asyncio-dev.html#asyncio-debug-mode
ENV PYTHONASYNCIODEBUG=1

WORKDIR /app

RUN python3 -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10002
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    coapuser

RUN dpkg-reconfigure -f noninteractive wireshark-common
RUN usermod -a -G wireshark coapuser
RUN sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/dumpcap
#RUN setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip' /usr/bin/dumpcap
#RUN chgrp wireshark /usr/bin/dumpcap
#RUN chmod 750 /usr/bin/dumpcap

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container.
COPY . .
RUN chown ${UID}:${UID} server.py

# Switch to the non-privileged user to run the application.
USER coapuser

# Expose the port that the application listens on.
EXPOSE 5683 5683/udp
EXPOSE 80 80/udp

# Difference between RUN and CMD

# Run the server
CMD python3 server.py
#ENTRYPOINT ["mysql"]

# Run the application.
#CMD gunicorn 'authentication-app.app:app' --bind=0.0.0.0:8000
#CMD flask --app authentication --debug run --host 0.0.0.0 --port 8000
#CMD [ "flask", "--app", "app", "--debug", "run", "--port", "8000" ]