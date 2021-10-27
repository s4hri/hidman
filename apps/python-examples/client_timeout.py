from hidman.core import HIDClient, HIDKeyboard


dev = HIDClient(address="tcp://localhost:6666")

while True:
    print(dev.waitEvent(timeout_ms=3000))
