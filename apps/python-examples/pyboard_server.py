from hidman.core import HIDServer
import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
selected_device = None
if '/dev/input/hidman0' in evdev.list_devices():
    selected_device = '/dev/input/hidman0'
else:
    for device in devices:
        if 'MicroPython' in device.name:
            selected_device = device.path

serv = HIDServer(device=selected_device, address="tcp://*:6666")
serv.run()
