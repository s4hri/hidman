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
        if device:
            self._device = InputDevice(device)
        else:
            self._device = device

    def clear(self):
        if self._device:
            while not self._device.read_one() is None:
                return
        return

    def waitEvent(self, event_type=None, event_code=None, event_value=None, timeout_ms=None, clear_events=True):

        if clear_events:
            self.clear()
        if self._device:
            # In order to respect REQ and REP archetypes in ZMQ the client should receive a reply right before the timeout
            if timeout_ms is None:
                r = True
            else:
                r, w, x = select([self._device], [], [], timeout_ms/1000.0 - 0.01)
            if r:
                for event in self._device.read_loop():
                    if not event_type is None:
                        if event.type == event_type:
                            data = categorize(event)
                            if not event_value is None:
                                if data.keystate == event_value:
                                    return (data.keystate, data.keycode, ecodes.EV_KEY)
                                    if not event_code is None:
                                        if event_code == data.keycode:
                                            return (data.keystate, data.keycode, ecodes.EV_KEY)
                                    else:
                                        return (data.keystate, data.keycode, ecodes.EV_KEY)
                            else:
                                return (data.keystate, data.keycode, ecodes.EV_KEY)
                    else:
                        return (event.code, event.value)
            else: #Timeout reached
                return None
        else:
            return None

    def close(self):
        if self._device:
            self._device.close()

class HIDServer:

    def __init__(self, device=None, address="ipc://pyboard"):
        self._device = HIDDevice(device)
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(address)
        self._socket_lock = threading.Lock()

    def reply(self, req):
        res = self._device.waitEvent(event_type=req[0], event_code=req[1], event_value=req[2], timeout_ms=req[3])
        with self._socket_lock:
            self._socket.send_pyobj(res)

    def run(self):
        while True:
            req = self._socket.recv_pyobj()
            if req is None:
                self._device.close()
                return
            self.reply(req) #TODO: consider the reply call for multi-threading in the future

class HIDKeyboard:
    KEY_UP = 0
    KEY_DOWN = 1
    KEY_HOLD = 2

class HIDClient:

    def __init__(self, address="ipc://pyboard"):
        self._address = address
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.connect(self._address)

    def waitEvent(self, event_type=None, event_code=None, event_value=None, timeout_ms=None):
        t0 = time.perf_counter()
        self._socket.send_pyobj([event_type, event_code, event_value, timeout_ms])
        poller = zmq.Poller()
        poller.register(self._socket, zmq.POLLIN)
        if poller.poll(timeout_ms):
            msg = self._socket.recv_pyobj()
        else:
            msg = None
        return (msg, time.perf_counter()-t0)

    def waitKey(self, evkey=None, evstate=None, timeout_ms=None):
        return self.waitEvent(event_type=ecodes.EV_KEY, event_code=evkey, event_value=evstate, timeout_ms=timeout_ms)

    def waitKeyPress(self, evkey=None, evstate=HIDKeyboard.KEY_DOWN, timeout_ms=None):
        return self.waitEvent(event_type=ecodes.EV_KEY, event_code=evkey, event_value=evstate, timeout_ms=timeout_ms)

    def waitKeyRelease(self, evkey=None, evstate=HIDKeyboard.KEY_UP, timeout_ms=None):
        return self.waitEvent(event_type=ecodes.EV_KEY, event_code=evkey, event_value=evstate, timeout_ms=timeout_ms)

    def close(self):
        self._socket.send_pyobj(None)

    def __del__(self):
        self._socket.disconnect(self._address)
