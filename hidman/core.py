from evdev import InputDevice, categorize, ecodes
import evdev
import time
import zmq
import statistics
import logging
import threading
from select import select

class HIDDevice:

    def __init__(self, device=None):
        self._device = InputDevice(device)

    def clear(self):
        while not self._device.read_one() is None:
            return

    def read(self):
        return self._device.read_one()

    def close(self):
        self._device.close()

class HIDEvent:

    KEY_UP = 0
    KEY_DOWN = 1
    KEY_HOLD = 2

    @staticmethod
    def parse(event, event_type=None, event_code=None, event_status=None):
        if event_type and event.type == ecodes.EV_KEY:
            data = categorize(event)
            if event_status is None:
                if not event_code is None:
                    if data.keycode in event_code:
                        return (data.keystate, data.keycode, ecodes.EV_KEY)
                else:
                    return (data.keystate, data.keycode, ecodes.EV_KEY)
            else:
                if data.keystate == event_status and not event_code is None:
                    if data.keycode in event_code:
                        return (data.keystate, data.keycode, ecodes.EV_KEY)

        return None


class HIDServer:

    def __init__(self, device, address="ipc://pyboard"):
        self._device = HIDDevice(device)
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PAIR)
        self._socket.bind(address)

    def run(self):
        while True:
            event = self._device.read()
            if event:
                data = categorize(event)
                self._socket.send_pyobj(event)

    def __del__(self):
        self._device.close()

class HIDClient:

    def __init__(self, address="ipc://pyboard"):
        self._address = address
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PAIR)
        self._socket.connect(self._address)

    def waitEvent(self, event_type=None, event_code=None, event_status=None, timeout_ms=None):
        t0 = time.perf_counter()
        if not timeout_ms is None:
            poller = zmq.Poller()
            poller.register(self._socket, zmq.POLLIN)
        res = None
        while res is None:
            if not timeout_ms is None:
                elapsed_time = (time.perf_counter() - t0)*1000.0
                if timeout_ms <= elapsed_time:
                    break
                elif poller.poll(timeout_ms-elapsed_time):
                    event = self._socket.recv_pyobj()
                    res = HIDEvent.parse(event, event_type, event_code, event_status)
                else:
                    break
            else:
                event = self._socket.recv_pyobj()
                res = HIDEvent.parse(event, event_type, event_code, event_status)

        return (res, time.perf_counter()-t0)

    def waitKey(self, keyList=None, evstate=None, timeout_ms=None):
        return self.waitEvent(event_type=ecodes.EV_KEY, event_code=keyList, event_status=evstate, timeout_ms=timeout_ms)

    def waitKeyPress(self, keyList=None, evstate=HIDEvent.KEY_DOWN, timeout_ms=None):
        return self.waitEvent(event_type=ecodes.EV_KEY, event_code=keyList, event_status=evstate, timeout_ms=timeout_ms)

    def waitKeyRelease(self, keyList=None, evstate=HIDEvent.KEY_UP, timeout_ms=None):
        return self.waitEvent(event_type=ecodes.EV_KEY, event_code=keyList, event_status=evstate, timeout_ms=timeout_ms)

    def close(self):
        self._socket.send_pyobj(None)

    def __del__(self):
        self._socket.disconnect(self._address)
