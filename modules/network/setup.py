#!/usr/bin/env python
'''Set up the network config files'''
from __future__ import print_function
import ConfigParser
import tempfile
import sys
import os

# Thanks to ssokolow from http://stackoverflow.com/questions/2761829
def get_default_gateway_linux():
    with open('/proc/net/route') as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return fields[0]

def get_interfaces_linux():
    is_physical = lambda i: os.path.isdir('/sys/class/net/{}/device'.format(i))
    return filter(is_physical, os.listdir('/sys/class/net'))

def create_interfaces_configurator(module):
    config = ConfigParser.SafeConfigParser()
    for iface in get_interfaces_linux():
        config.read('{}.cfg'.format(module))
        config.set('DEFAULT', 'interface', iface)
        
        if iface == get_default_gateway_linux():
            config.set('DEFAULT', 'default_gw', '(default)')
            config.set('config', 'hide', str(False))
            
        with tempfile.NamedTemporaryFile(prefix = module, delete = False) as fd:
            config.write(fd)

        yield fd.name

def setup(module):
    map(print, create_interfaces_configurator(module))
    
try:    
    os.chdir(os.path.dirname(__file__))
    setup(os.path.abspath(__file__).split('/')[-2])
    
except Exception as inst:
    print("Unable to set up network interfaces: {}".format(inst), sys.stderr)
    sys.exit(1)
