from evdev import InputDevice, categorize, ecodes
import time
import zmq

class HIDDevice:

    def __init__(self, device):
        self._dev = InputDevice(device)

    def waitEvent(self):
        for event in self._dev.read_loop():
            return event

    def close(self):
        self._dev.close()

class HIDServer:

    def __init__(self, device='/dev/input/pyboard', address="ipc://pyboard"):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(address)
        self._device = HIDDevice(device)

    def run(self):
        while True:
            msg = self._socket.recv()
            if msg == b'exit':
                self._device.close()
                return
            res = self._device.waitEvent()
            self._socket.send(b"rep")


class HIDClient:

    def __init__(self, address="ipc://pyboard"):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(address)

    def waitEvent(self):
        t0 = time.perf_counter()
        self._socket.send(b"req")
        message = self._socket.recv()
        duration = time.perf_counter() - t0
        return duration

    def __del__(self):
        self._socket.send(b"exit")
