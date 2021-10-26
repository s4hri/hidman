import sys
import getopt

import time
from random import random as rand

from hidman.core import HIDClient
from pylsl import StreamInfo, StreamOutlet, local_clock

import io, os
import re
import threading

class DevHelper:

    KEYS_MAP = ["KEY_1", "KEY_2", "KEY_3", "KEY_4"]

    def __init__(self):
        self._capturing = True
        self._sample = [0, 0, 0, 0]
        self._dev = HIDClient(address="tcp://localhost:6666")
        self._worker = threading.Thread(target=self.worker).start()

    def update(self, sample):
        i = DevHelper.KEYS_MAP.index(sample[0][1])
        self._sample[i] = int(sample[0][0] > 0)/2

    def worker(self):
        while self._capturing:
            sample = self._dev.waitKey()
            self.update(sample)

    def getSample(self):
        return self._sample

    def stop(self):
        self._capturing = False
        self._worker.join()

def main(argv):
    dev = DevHelper()
    srate = 100
    name = 'Key events [1, 2, 3, 4]'
    type = 'Key Events'
    channel_names = ["1", "2", "3", "4"]
    n_channels = len(channel_names)
    help_string = 'lsl-client.py -s <sampling_rate> -n <stream_name> -t <stream_type>'
    try:
        opts, args = getopt.getopt(argv, "hs:n:t:", longopts=["srate=", "name=", "type"])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt in ("-s", "--srate"):
            srate = float(arg)
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-t", "--type"):
            type = arg

    # first create a new stream info (here we set the name to BioSemi,
    # the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available (you
    # could also omit it but interrupted connections wouldn't auto-recover).
    info = StreamInfo(name, type, n_channels, srate, 'float32', 's4hri_keys')

    # append some meta-data
    info.desc().append_child_value("manufacturer", "MicroPython")
    chns = info.desc().append_child("channels")
    for label in channel_names:
        ch = chns.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("unit", "m/s^2")
        ch.append_child_value("type", "Key Events")

    # next make an outlet; we set the transmission chunk size to 32 samples and
    # the outgoing buffer size to 360 seconds (max.)
    outlet = StreamOutlet(info, 32, 360)

    print("now sending data...")
    start_time = local_clock()
    sent_samples = 0
    while True:
        elapsed_time = local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        if required_samples > 0:
            # make a chunk==array of length required_samples, where each element in the array
            # is a new random n_channels sample vector
            mychunk = [dev.getSample() for samp_ix in range(required_samples)]
            # get a time stamp in seconds (we pretend that our samples are actually
            # 125ms old, e.g., as if coming from some external hardware)
            stamp = local_clock()
            # now send it and wait for a bit
            outlet.push_chunk(mychunk, stamp)
            sent_samples += required_samples
        time.sleep(0.01)

    capturing = False
    dev.stop()


if __name__ == '__main__':
    main(sys.argv[1:])
