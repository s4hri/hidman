from hidman.core import HIDServer

serv = HIDServer(device='/dev/input/hidman0', address="tcp://*:6666")
serv.run()
