from evdev import InputDevice, categorize, ecodes
import time
import zmq
import statistics
import logging

class HIDDevice:

    def __init__(self, device=None):
        if device:
            self._device = InputDevice(device)
        else:
            self._device = device

    def waitEvent(self):
        if self._device:
            for event in self._device.read_loop():
                return event

    def close(self):
        if self._device:
            self._device.close()

class HIDServer:

    def __init__(self, device=None, address="ipc://pyboard", logging_level=logging.DEBUG):
        self._device = HIDDevice(device)
        self._logger = logging.getLogger('hidman')
        self._logger.setLevel(logging_level)
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(address)

    def run(self):
        while True:
            msg = self._socket.recv()
            if msg == b'exit':
                return self._device.close()
            res = self._device.waitEvent()
            self._socket.send_pyobj(res)


class HIDClient:

    def __init__(self, address="ipc://pyboard"):
        self._address = address
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.connect(self._address)

    def waitEvent(self, timeout_ms=None):
        self._socket.send(b"req")
        poller = zmq.Poller()
        poller.register(self._socket, zmq.POLLIN)
        if poller.poll(timeout_ms):
            msg = self._socket.recv_pyobj()
        else:
            print("timeout")
            msg = None
        return msg

    def __del__(self):
        self._socket.send(b"exit")
        self._socket.disconnect(self._address)
