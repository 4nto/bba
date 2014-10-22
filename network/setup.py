'''Set up the network config files'''
from __future__ import print_function
import ConfigParser
import shutil
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

def get_interfaces_linux(blacklist):
    blacklisting = lambda iface: filter(lambda b: b == iface, blacklist) == []
    return filter(blacklisting, os.listdir('/sys/class/net'))

config = ConfigParser.SafeConfigParser()
default_gw = get_default_gateway_linux()

def create_interfaces_configurator():
    '''Remove last created files'''
    for fname in filter (lambda fname: 'network-' in fname, os.listdir('network')):
        os.remove('network/{}'.format(fname))

    '''Do not consider "lo" interface and interface without physical addr (virtual)'''
    for iface in get_interfaces_linux(['lo']):
        fname = 'network/network-{}.cfg'.format(iface)
        shutil.copyfile('network/network.cfg', fname)

        config.read(fname)    
        config.set('DEFAULT', 'interface', iface)    
        if iface == default_gw:
            config.set('DEFAULT', 'default_gw', '(default)')
            config.set('config', 'hide', str(False))
            
        with open(fname, 'wb') as f:
            config.write(f)

        yield fname

try:
    map(print, create_interfaces_configurator())
except Exception as inst:
    print("Unable to set up network interfaces")
    print("Unable to set up network interfaces: {}".format(inst), sys.stderr)
    sys.exit(1)
