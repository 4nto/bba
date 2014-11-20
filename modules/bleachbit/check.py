#!/usr/bin/env python
'''Get how many files bleachbit will remove'''
from __future__ import print_function
import ConfigParser
import subprocess
import signal
import shlex
import sys
import os

patterns = ['Files to be deleted:', 'File da eliminare:']

def check(proc):
    (output, error) = proc.communicate()
    for line in reversed(output.splitlines()):
        if filter(lambda pattern: pattern in line, patterns) != []:
            break
        
    try: 
        file_to_delete = int(line.split(':')[1].strip())
    except:
        print("Unable to verify your data")        
        print("Parsing error", file=sys.stderr)
        sys.exit(2)
        
    if file_to_delete == 0:
        print("Your system is clean")        
        sys.exit(1)

    verb, name = ('is', 'file') if file_to_delete == 1 else ('are', 'files')
    print("There {} {} {} to remove".format(verb, file_to_delete, name))

try:
    os.chdir(os.path.dirname(__file__))
    config = ConfigParser.SafeConfigParser(allow_no_value = True)    
    config.read('bleachbit.cfg')
    bleachbit = config.get('DEFAULT', 'bleachbit')
    cleaners = config.get('DEFAULT', 'cleaners')    
    cmd = "{} -p -c {}".format(bleachbit, cleaners)
    proc = subprocess.Popen(shlex.split(cmd),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    check(proc)
    
except KeyboardInterrupt:
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    print("Unable to verify your data")
    sys.exit(2)
    
except Exception as inst:
    print("Unable to verify your data")
    print("Unknown_error: {}".format(inst), file=sys.stderr)    
    sys.exit(2)  
