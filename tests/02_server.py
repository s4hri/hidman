from hidman.core import HIDServer


serv = HIDServer(address="tcp://*:5555")
serv.run()
