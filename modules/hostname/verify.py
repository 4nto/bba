'''Verify the hostname module'''
from __future__ import print_function
import ConfigParser
import random
import sys
import os

cfg = 'hostname/hostname.cfg'

def randomize(fname):
    '''From the given dictionary file return a random hostname'''
    if not os.path.isfile(fname):
        raise Exception("Randomize dictionary file {} not found".format(fname))
        
    with open(fname) as f:
        f.seek(random.randint(0, os.stat(fname).st_size))
        return randomize(fname) if f.readline() == "" else f.readline()
        
try:
    config = ConfigParser.SafeConfigParser()
    config.read(cfg)
    config.set('cmd', 'random', randomize('/etc/dictionaries-common/words'))    
    with open(cfg, 'wb') as fd:
        config.write(fd)
except KeyboardInterrupt:
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    print("Unable to configure hostname module")
    sys.exit(1) 
except Exception as inst:
    print("Unknown_error: {}".format(inst), file=sys.stderr)
    print("Unable to configure hostname module")    
    sys.exit(1)
