import asyncio
from evdev import InputDevice, categorize, ecodes

print("Waiting for input events...")

dev = InputDevice('/dev/input/pyboard')

async def helper(dev):
    async for ev in dev.async_read_loop():
        print(repr(ev))

loop = asyncio.get_event_loop()
loop.run_until_complete(helper(dev))
