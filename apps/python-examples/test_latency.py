import threading
import time
import statistics
import sys
sys.path.append("..")

from hidman.core import HIDServer, HIDClient

serv = HIDServer(device=None)
t = threading.Thread(target=serv.run)
t.start()
client = HIDClient()
trials = []
for i in range(0,1000):
    trials.append(client.waitEvent()[1])
print("Latency mean=%.6f std=%.6f" % (statistics.mean(trials), statistics.stdev(trials)) )
client.close()
