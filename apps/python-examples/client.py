from hidman.core import HIDClient


dev = HIDClient(address="tcp://localhost:6666")

print(dev.waitKey())
print(dev.waitKey(keyList=['KEY_1']))
print(dev.waitKeyPress(keyList=['KEY_2', 'KEY_3']))
print(dev.waitKeyRelease(keyList=['KEY_4']))
