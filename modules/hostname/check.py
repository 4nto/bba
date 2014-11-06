'''Check the passed argument hostname with the current hostname'''
from __future__ import print_function
import socket
import sys

if len(sys.argv) != 2:
    print("Bad command line arguments", file=sys.stderr)
    print("Unable to retrieve your last boot hostname")
    sys.exit(2)

def check(hostname):
    if hostname == socket.gethostname():
        print("Hostname {} is the same from the last boot".format(hostname))
        sys.exit(1)
        
    print("Hostname {} is different from the last boot {}".format(socket.gethostname(), hostname))        
    

try:
    check(sys.argv[1])
except KeyboardInterrupt:
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    print("Unable to retrieve your last boot hostname")
    sys.exit(2)
except Exception as inst:
    print("Unknown_error: {}".format(inst), file=sys.stderr)
    print("Unable to retrieve your last boot hostname")
    sys.exit(2)
