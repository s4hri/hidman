import asyncio
import evdev

from evdev import InputDevice, categorize, ecodes

selected_device = evdev.InputDevice('/dev/input/hidman0')
print("Listening input events from {}".format(selected_device))
for event in selected_device.read_loop():
    print(evdev.categorize(event))
