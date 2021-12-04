from evdev import InputDevice, categorize, ecodes
import evdev
import time
import zmq
import threading

class HIDEvent:

    KEY_UP = 0
    KEY_DOWN = 1
    KEY_HOLD = 2

    @staticmethod
    def parse(event, event_type=None, event_code=None, event_status=None):
        if event is None:
            return None
        elif event == 0:
            return "TEST"
        elif event_type and event.type == ecodes.EV_KEY:
            data = categorize(event)
            if event_status is None:
                if not event_code is None:
                    if data.keycode in event_code:
                        return (data.keystate, data.keycode, ecodes.EV_KEY)
                else:
                    return (data.keystate, data.keycode, ecodes.EV_KEY)
            else:
                if data.keystate == event_status:
                    if event_code is None:
                        return (data.keystate, data.keycode, ecodes.EV_KEY)
                    elif data.keycode in event_code:
                        return (data.keystate, data.keycode, ecodes.EV_KEY)
        return None

class HIDDevice:

    POLLING_TIME_MS = 1

    def __init__(self, device=None):
        if not device is None:
            self._device = InputDevice(device)
        else:
            self._device = device

    def clear(self):
        if not self._device is None:
            while not self._device.read_one() is None:
                return

    def close(self):
        if not self._device is None:
            self._device.close()

    def readLoop(self):
        if not self._device is None:
            return self._device.read_loop()

    def readOne(self):
        if not self._device is None:
            return self._device.read_one()
        return 0 #virtual event for testing purposes

    def waitEvent(self, event_type=None, event_code=None, event_status=None, timeout_ms=None):
        t0 = time.perf_counter()
        res = None
        while res is None:
            elapsed_time = (time.perf_counter() - t0)*1000.0
            if not timeout_ms is None:
                if timeout_ms <= elapsed_time:
                    break
            event = self.readOne()
            res = HIDEvent.parse(event, event_type, event_code, event_status)
            time.sleep(HIDDevice.POLLING_TIME_MS/1000.0)
        return (res, elapsed_time)

    def waitKey(self, keyList=None, evstate=None, timeout_ms=None):
        return self.waitEvent(event_type=ecodes.EV_KEY, event_code=keyList, event_status=evstate, timeout_ms=timeout_ms)

    def waitKeyPress(self, keyList=None, evstate=HIDEvent.KEY_DOWN, timeout_ms=None):
        return self.waitEvent(event_type=ecodes.EV_KEY, event_code=keyList, event_status=evstate, timeout_ms=timeout_ms)

    def waitKeyRelease(self, keyList=None, evstate=HIDEvent.KEY_UP, timeout_ms=None):
        return self.waitEvent(event_type=ecodes.EV_KEY, event_code=keyList, event_status=evstate, timeout_ms=timeout_ms)


class HIDServer:

    def __init__(self, device=None, address="ipc://pyboard"):
        self._device = HIDDevice(device)
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind(address)
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            event = self._device.readOne()
            if not event is None:
                self._socket.send_pyobj(event)

    def close(self):
        self._running = False
        self._device.close()

    def __del__(self):
        self.close()

class HIDClient:

    def __init__(self, address="ipc://pyboard"):
        self._address = address
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        self._socket.connect(self._address)
        self._socket.setsockopt(zmq.SUBSCRIBE, b'')

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

    def __del__(self):
        self._socket.disconnect(self._address)
        self._socket.close()
