'''Get the last system startup hostname'''
import os
import sys
import socket

sys.path.append('.') 
from util.configuration import Configurator

config = Configurator('hostname/hostname.cfg')

def lookup(fname, cnt = 0):
    if cnt > 0:
        fname = '{}.{}'.format(fname[:-2] if cnt > 1 else fname, cnt)       

    if not os.path.isfile(fname):
        config.exit_with_error('file_not_found' if cnt == 0 else 'string_not_found')
    
    with open(fname) as f:
        startup_lines = filter (lambda line: "Linux version" in line, f)
        if len(startup_lines) == 0:
            lookup(fname, cnt + 1)
        else:
            try:
                hostname = startup_lines[-1].split()[3]
            except:
                config.exit_with_error('parsing_error')                
            else:
                sys.stdout.write(hostname)
                if hostname != socket.gethostname():
                    config.exit_with_error('ko')

try:
    lookup(config.get('config', 'kernel_log'))
except KeyboardInterrupt:
    config.exit_with_error('sigint_received')
