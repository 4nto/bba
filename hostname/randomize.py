'''Get a random name for the hostname'''
import os
import sys
import random

sys.path.append('.') 
from util.configuration import Configurator

config = Configurator('hostname/hostname.cfg')

def randomize(fname):
    if not os.path.isfile(fname):
        config.exit_with_error('file_not_found')
        
    total_bytes = os.stat(fname).st_size
    with open(fname) as f:
        f.seek(random.randint(0, total_bytes))
        if f.readline() == "":
            randomize(fname)
        else:
            sys.stdout.write(f.readline())
            sys.exit(0)

try:
    randomize(config.get('config', 'random'))
except KeyboardInterrupt:
    config.exit_with_error('sigint_received')
