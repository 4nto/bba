import os
import sys
import random
import socket
import signal

from __init__ import config
import anonymous

def randomize(fname):
    if not os.path.isfile(fname):
        config.exit_with_error('file_not_found')
        
    total_bytes = os.stat(fname).st_size
    with open(fname) as f:
        f.seek(random.randint(0, total_bytes))
        if f.readline() == "":
            randomize(fname)
        
        return f.readline().strip()

def run(new_hname):
    if new_hname == socket.gethostname():
        print ("Unuseful changing the hostname to the same one")
        sys.exit(0)

    '''Release DHCP address'''
    try:
        anonymous.clean_dhcp()
        print (" * DHCP address released")
    except:
        #config.exit_with_error()
        print " * Unable to release DHCP address"
        sys.exit(1)

    '''Change value in /etc/hosts'''
    try:
        with open('hosts', 'r+') as f:
            replace = f.read().replace(socket.gethostname(), new_hname)
            f.seek(0)
            f.write(replace)
            f.truncate()
        print (" * /etc/hosts updated")
    except:
        print " * Unable to update /etc/hosts"
        sys.exit(1)

    '''Start hostname service'''
    try:
        anonymous.service('hostname', 'start')
        print " * Service hostname started"
    except:
        print " * Service hostname not started"
        #sys.exit(1)        

try:
    hname = sys.argv[1] if len(sys.argv) > 1 else randomize(config.get('config', 'random'))
    run(hname)
except KeyboardInterrupt:
    config.exit_with_error('sigint_received')
