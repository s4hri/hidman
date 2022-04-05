import sys, getopt
from hidman.core import HIDServer

def main(argv):
   device = ""
   try:
       opts, args = getopt.getopt(argv,"hd:",["device="])
   except getopt.GetoptError:
      print('hidserver.py -d <device>')
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-d", "--device"):
          device = arg
          print('Device is: ', device)
          serv = HIDServer(device=device, address="tcp://*:6666")
          serv.run()
   print('hidserver.py -d <device>') 
   sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])

