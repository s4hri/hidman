ARG DOCKER_SRC

FROM ${DOCKER_SRC}
LABEL maintainer="Davide De Tommaso <davide.detommaso@iit.it>"

RUN apt-get update
RUN apt-get install -y python3-pip

RUN python3 -m pip install --upgrade pip

WORKDIR /usr/local/src/

COPY . hidman

RUN cd hidman && pip3 install -r requirements.txt && pip3 install .
