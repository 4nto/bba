#!/usr/bin/env python
'''Run bleachbit step by step'''
from __future__ import print_function
import ConfigParser
import subprocess
import signal
import shlex
import sys
import os
import re

def run(bleachbit, cleaner, pattern):
    cmd = "{} -c {}".format(bleachbit, cleaner)
    proc = subprocess.Popen(shlex.split(cmd),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    print("Bleachbit(ing) on {}..".format(' '.join(cleaner.split('.')).title()))
    (stdout, stderr) = proc.communicate()

    for line in reversed(stdout.splitlines()):
        if pattern in line:
            print('* ' + line)
            break
    
    if stderr.strip() != '':
        print("* Error: {}".stderr)    

try:
    os.chdir(os.path.dirname(__file__))
    config = ConfigParser.SafeConfigParser(allow_no_value = True)    
    config.read('bleachbit.cfg')
    bleachbit = config.get('DEFAULT', 'bleachbit')
    cleaners = config.get('DEFAULT', 'cleaners').split()
    pattern = config.get('config', 'pattern_op')
    wrun = lambda cleaner: run(bleachbit, cleaner, pattern)
    map(wrun, cleaners)

except KeyboardInterrupt:
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    print("Unable to clean all your data")
    sys.exit(2)
    
except Exception as inst:
    print("Unable to clean all your data")
    print("Unknown_error: {}".format(inst), file=sys.stderr)    
    sys.exit(2)  
