#!/usr/bin/python3

import sys, getopt
from hidman.core import HIDClient

def main(argv):
   device = ""
   try:
       opts, args = getopt.getopt(argv,"hs:",["serveraddress="])
   except getopt.GetoptError:
      print('hidclient.py -s <server-address>')
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-s", "--server-address"):
          server_address = arg
          print('Server address is: ', server_address)
          client = HIDClient(address="tcp://%s:6666" % server_address)
          while True:
              print(client.waitKey())
   print('hidclient.py -s <server_address>')
   sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
