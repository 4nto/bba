import os
import sys
import shutil
import ConfigParser
import netifaces as NI

sys.path.append('.') 
from util import get_default_gateway_linux

config = ConfigParser.SafeConfigParser()
default_gw = get_default_gateway_linux()

'''Remove last created files'''
for fname in filter (lambda fname: 'network-' in fname, os.listdir('network')):
    os.remove('network/{}'.format(fname))

'''Do not consider "lo" interface and interface without physical addr (virtual)'''
for iface in filter (lambda i: i != "lo" and NI.AF_LINK in NI.ifaddresses(i), NI.interfaces()):
    fname = 'network/network-{}.cfg'.format(iface)
    shutil.copyfile('network/network.cfg', fname)
    config.read(fname)
    config.set('DEFAULT', 'interface', iface)
    config.set('DEFAULT', 'default_gw', '(default)' if iface == default_gw else '')
    with open(fname, 'wb') as f:
        config.write(f)

