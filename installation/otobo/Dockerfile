FROM ubuntu:latest

RUN apt-get update
COPY setup-locally.sh /usr/local/bin/install.sh
COPY overwrite /tmp/installation
COPY otobo-docker /tmp/installing-docker.sh
RUN chmod +x /usr/local/installing-docker.sh

COPY otobo-docker /tmp/installing-docker-images.sh
RUN chmod +x /usr/local/installing-docker-images.sh

RUN /usr/local/bin/installing-docker.sh

RUN /usr/local/bin/installing-docker-images.sh

ENV OTOBO_WEB_VOLUME="/var/lib/docker/volumes/otobo_opt_otobo/_data"
ENV LOCAL_DIR="/tmp/installation"
ENV OTOBO_DIR="/opt/otobo-docker"
ENV OVERWRITE=1
ENV OTOBO_DB_ROOT_PASSWORD=1234

CMD ["tail", "-f", "/dev/null"]