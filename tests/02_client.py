from hidman.core import HIDClient


dev = HIDClient(address="tcp://localhost:5555")

for i in range(0,10):
    print(dev.waitEvent())
