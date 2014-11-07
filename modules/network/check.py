#!/usr/bin/env python
'''Check the current mac addr'''
from __future__ import print_function
import subprocess
import shlex
import sys
import re

if len(sys.argv) != 2:
    print("Unable to check your MAC address")     
    print("Bad use of the command", file=sys.stderr)
    sys.exit(2)

def check(proc):
    pattern = re.compile (r"([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", re.I)
    (stdout, stderr) = proc.communicate()
    try:
        macs = map (lambda line: pattern.search(line).group(), stdout.strip().splitlines())
    except:
        print("Unable to check your MAC address")        
        print("Parsing error", file=sys.stderr)
        sys.exit(2)
    else:        
        if macs[1:] == macs[:-1]:            
            print("{} MAC address {} is REAL".format(sys.argv[1], macs[:-1][0]))
            sys.exit(1)

        print("{} MAC address {} is SPOOFED".format(sys.argv[1], macs[:-1][0]))

try:
    cmd = "macchanger -s {}".format(sys.argv[1])
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check(proc)
except KeyboardInterrupt:
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    print("Unable to check your MAC address")
    sys.exit(2)
except Exception as inst:
    print("Unable to check your MAC address")
    print("Unknown_error: {}".format(inst), file=sys.stderr)    
    sys.exit(2)    
