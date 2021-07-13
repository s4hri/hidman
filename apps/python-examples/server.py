from hidman.core import HIDServer
import evdev

selected_device = evdev.InputDevice('/dev/input/hidman0')
serv = HIDServer(device=selected_device, address="tcp://*:6666")
serv.run()
