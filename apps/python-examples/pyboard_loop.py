import asyncio
import evdev

from evdev import InputDevice, categorize, ecodes

print("Listing all the input devices...")
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)

print("Properties of the selected input device...")
device = evdev.InputDevice('/dev/input/hidman0')
print(device)

print("Waiting for input events...")
for event in device.read_loop():
    print(evdev.categorize(event))
