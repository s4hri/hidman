import pytest
import threading
import time
import statistics

from hidman.core import HIDServer, HIDClient


class TestLatency:

    def test_run(self):
        serv = HIDServer(device=None)
        t = threading.Thread(target=serv.run)
        t.start()
        client = HIDClient()
        client.waitEvent()
        client.close()
