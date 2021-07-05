import asyncio
import evdev

from evdev import InputDevice, categorize, ecodes

print("Listing all the input devices...")
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)

selected_device = None
if '/dev/input/hidman0' in evdev.list_devices():
    selected_device = '/dev/input/hidman0'
else:
    for device in devices:
        if 'MicroPython' in device.name:
            selected_device = device.path

if selected_device:
    print("Properties of the selected input device...")
    device = evdev.InputDevice(selected_device)
    print(device)

    print("Waiting for input events...")
    for event in device.read_loop():
        print(evdev.categorize(event))
else:
    print("No MicroPython device found. Please link a MicroPython board to /dev/input/hidman0")
