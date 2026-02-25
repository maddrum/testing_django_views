FROM python:3.12.12-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DOCKYARD_PROJECT_DIR=/opt
ENV DOCKYARD_USER=docker

RUN groupadd -r $DOCKYARD_USER -g 1000 \
	&& useradd -u 1000 -r -g $DOCKYARD_USER -d $DOCKYARD_PROJECT_DIR -s /sbin/nologin -c "Docker image user" $DOCKYARD_USER \
	&& chown -R $DOCKYARD_USER:$DOCKYARD_USER $DOCKYARD_PROJECT_DIR

ENV PATH $PATH:$DOCKYARD_PROJECT_DIR/.local/bin
COPY .bashrc /etc/bash.bashrc
COPY entrypoint.sh /docker/entrypoint.sh
COPY run-server.sh /docker/run-server.sh

# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y  \
    nano \
    gettext \
    python3-dev build-essential

RUN apt-get update \
	&& apt-get install -y \
	python3-setuptools python3-distutils python3-pip python3-ipython \
	build-essential git-core gcc \
	cmake musl-dev

RUN pip3 install packaging

VOLUME $DOCKYARD_PROJECT_DIR
WORKDIR $DOCKYARD_PROJECT_DIR

USER $DOCKYARD_USER

EXPOSE 8000

ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["/docker/run-server.sh"]
