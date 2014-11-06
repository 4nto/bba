'''Get how many files bleachbit will remove'''
from __future__ import print_function
import subprocess
import signal
import shlex
import sys
import os

bleachbit = '/usr/bin/bleachbit'
patterns = ['Files to be deleted:', 'File da eliminare:']

if len(sys.argv) < 2:
    print("Unable to verify your data")     
    print("Bad use of the command", file=sys.stderr)
    sys.exit(2)

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
        
    if file_to_delete != '0':
        print("There are {} files to remove".format(file_to_delete))
        sys.exit(1)

    print("Your system is clean")

try:
    cmd = "{} -p -c {}".format(bleachbit, " ".join(sys.argv[1:]))
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check(proc)
except KeyboardInterrupt:
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    print("Unable to verify your data")
    sys.exit(2)
except Exception as inst:
    print("Unable to verify your data")
    print("Unknown_error: {}".format(inst), file=sys.stderr)    
    sys.exit(2)  
