#!/usr/bin/env python
'''Verify the network module'''
from __future__ import print_function
import subprocess
import sys
import os

def check_virtualization():
    command_exist = lambda fpath: os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    if os.getuid() == 0 and command_exist('/usr/sbin/virt-what'):
        proc = subprocess.Popen('/usr/sbin/virt-what',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        
        (stdout, stderr) = proc.communicate()
        
        if stdout != '' or stderr != '':
            return True

    return False   

try:
    if check_virtualization():
        print("Unable to change MAC addr on virtualized systems")
        sys.exit(1)    

except KeyboardInterrupt:
    print("Unable to verify module configuration\n")
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    sys.exit(1)
    
except Exception as inst:
    print("Unable to verify module configuration\n")
    print("Unknown error during verification: {}\n".format(inst), file=sys.stderr)
    sys.exit(1)
