#!/usr/bin/env python
'''Setup the hostname config file'''
from __future__ import print_function
import ConfigParser
import tempfile
import random
import sys
import os

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

def randomize(fname):
    '''From the given dictionary file return a random hostname'''
    if not os.path.isfile(fname):
        raise Exception("Randomize dictionary file {} not found".format(fname))
        
    with open(fname) as f:
        f.seek(random.randint(0, os.stat(fname).st_size))
        return randomize(fname) if f.readline() == "" else f.readline()

def setup(module):    
    config = ConfigParser.SafeConfigParser()
    config.read('{}.cfg'.format(module))
    config.set('cmd', 'hostname', lookup(config.get('config', 'kernel_log')))
    config.set('cmd', 'random', randomize(config.get('config', 'random')))
    
    with tempfile.NamedTemporaryFile(prefix = module, delete = False) as fd:
        config.write(fd)

    print(fd.name)
        
try:
    os.chdir(os.path.dirname(__file__))
    setup(os.path.abspath(__file__).split('/')[-2])
    
except KeyboardInterrupt:
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    sys.exit(1)
    
except Exception as inst:
    '''It was unable to find the last boot hostname'''
    print("Unknown_error: {}".format(inst), file=sys.stderr)
    sys.exit(1)
    
        
    
