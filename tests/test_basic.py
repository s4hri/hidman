import pytest
import threading
import time
import statistics

from hidman.core import HIDServer, HIDClient, HIDDevice


class TestLatency:

    def test_run(self):
        serv = HIDServer(device=None)
        t = threading.Thread(target=serv.run)
        t.start()
        client = HIDClient()
        trials = []
        for i in range(0,1000):
            t0 = time.perf_counter()
            client.waitEvent()
            trials.append(time.perf_counter() - t0)
        print(statistics.variance(trials))


t = TestLatency()
t.test_run()
