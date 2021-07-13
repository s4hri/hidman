# hidman
Human Interface Device Manager

Client-server architecture for sharing evdev events in a network using ZeroMQ.

# Building the docker container

    $ cd hidman
    $ docker-compose build

# Runnning examples

    $ cd apps
    $ docker-compose -f <app.yml> up

## Testing latency

In order to test latency of the ZeroMQ client-server please execute:

    $ docker-compose -f test_latency.yml up

## Local events

In order to test the correct reception of evdev raw events please type the following:

    $ docker-compose -f input_loop.yml up

This requires an evdev device chosen among the ones in '/dev/input/event*'. You can select your preferred device in the .env file in hidman/apps

## Client-server

In order to test client and server in two docker containers please execute:

    $ docker-compose -f client_server.yml up

In this example the client waits for an event by calling waitEvent() remotely on the server.
