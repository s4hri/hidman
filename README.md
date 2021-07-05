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

    $ docker-compose -f apps/test_latency.yml up

## Local events

In order to test the visibility of events using pure evdev.read_loop() please execute:

    $ docker-compose -f apps/pyboard_inputs.yml up

This requires either a device `/dev/input/hidman0` linked to a chosen MicroPython board,
or a MicroPython device identifiable by name as `/dev/input/event*`

## Client-server

In order to test client and server in two docker containers please execute:

    $ docker-compose -f apps/pyboard_client_server.yml up

This requires either a device `/dev/input/hidman0` linked to a chosen MicroPython board,
or a MicroPython device identifiable by name as `/dev/input/event*`


