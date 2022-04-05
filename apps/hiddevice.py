import sys, getopt
from hidman.core import HIDDevice

def main(argv):
   device = ""
   try:
       opts, args = getopt.getopt(argv,"hd:",["device="])
   except getopt.GetoptError:
      print('hiddevice.py -d <device>')
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-d", "--device"):
          device = arg
          print('Device is: ', device)
          dev = HIDDevice(device=device)
          while True:
             print(dev.waitKey())
          dev.close()
   print('hiddevice.py -d <device>') 
   sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
