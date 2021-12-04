import threading
import time
import statistics

from hidman.core import HIDDevice

device = HIDDevice(device='/dev/input/hidman0')
print(device.waitKeyPress(timeout_ms=2000))
print(device.waitKeyRelease(timeout_ms=2000))
device.close()
