import threading
import time
import statistics

from hidman.core import HIDServer, HIDClient

serv = HIDServer(address="tcp://*:6666")
t = threading.Thread(target=serv.run)
t.start()
client = HIDClient(address="tcp://localhost:6666")
trials = []
for i in range(0,5000):
    trials.append(client.waitEvent()[1])
print("Latency mean=%.6f std=%.6f" % (statistics.mean(trials), statistics.stdev(trials)) )
serv.close()
t.join()
