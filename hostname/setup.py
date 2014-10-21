'''Setup the hostname config file'''
from __future__ import print_function
import ConfigParser
import sys
import os

cfg = 'hostname/hostname.cfg'

def lookup(fname, cnt = 0):    
    '''Find the last boot hostname'''
    if cnt > 0:
        fname = '{}.{}'.format(fname[:-2] if cnt > 1 else fname, cnt)

    if not os.path.isfile(fname):        
        raise Exception("Kernel log {} not found".format(fname)) if cnt == 0\
              else Exception("Evidence not found in {}".format(fname))
    
    with open(fname) as f:
        startup_lines = filter (lambda line: "Linux version" in line, f)
        return lookup(fname, cnt + 1) if len(startup_lines) == 0 else\
               startup_lines[-1].split()[3]
        
try:
    config = ConfigParser.SafeConfigParser()
    config.read(cfg)
    config.set('cmd', 'hostname', lookup('/var/log/kern.log'))
    with open(cfg, 'wb') as fd:
        config.write(fd)
    print(cfg)
except KeyboardInterrupt:
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    sys.exit(1) 
except Exception as inst:
    print("Unknown_error: {}".format(inst), file=sys.stderr)
    sys.exit(1)
