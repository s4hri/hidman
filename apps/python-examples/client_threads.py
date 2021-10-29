from hidman.core import HIDClient
import threading

c1 = HIDClient(address="tcp://localhost:6666")
c2 = HIDClient(address="tcp://localhost:6666")


def waitKey(client):
    tid = threading.currentThread().ident
    print("THREAD %d started", tid)
    print(client.waitKeyPress(keyList=['KEY_1'], timeout_ms=5000), tid)


t1 = threading.Timer(0.0, waitKey, args=(c1,))
t2 = threading.Timer(1.0, waitKey, args=(c2,))
t1.start()
t2.start()
t1.join()
t2.join()
