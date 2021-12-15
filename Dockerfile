ARG DOCKER_SRC

FROM ${DOCKER_SRC}
LABEL maintainer="Davide De Tommaso <davide.detommaso@iit.it>"

USER root

RUN apt-get update
RUN apt-get install -y python3-pip

USER docky
RUN python3 -m pip install --upgrade pip

COPY . hidman

RUN cd hidman && pip3 install .
