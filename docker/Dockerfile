ARG DOCKER_SRC

FROM ${DOCKER_SRC}
LABEL maintainer="Davide De Tommaso <davide.detommaso@iit.it>"

USER root

WORKDIR /app

RUN git clone https://github.com/s4hri/hidman &&\
    cd hidman &&\
    pip3 install .

ENV PYTHONPATH $PYTHONPATH:/app/hidman
