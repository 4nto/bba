import os
import sys
import shutil
import ConfigParser
import netifaces as NI

# Thanks to ssokolow from http://stackoverflow.com/questions/2761829
def get_default_gateway_linux():
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return fields[0]

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
    if iface == default_gw:
        config.set('DEFAULT', 'default_gw', '(default)')
        config.set('config', 'hide', str(False))
        
    with open(fname, 'wb') as f:
        config.write(f)

