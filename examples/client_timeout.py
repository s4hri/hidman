from hidman.core import HIDClient


dev = HIDClient(address="tcp://localhost:6666")

i = 0
while True:
    i=i+1
    print(i, dev.waitKeyRelease(keyList=['KEY_1'], timeout_ms=3000))
