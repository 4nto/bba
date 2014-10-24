'''Set up the network config files'''
from __future__ import print_function
import ConfigParser
import subprocess
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
'''
def get_interfaces_linux(blacklist):
    blacklisting = lambda iface: filter(lambda b: b == iface, blacklist) == []
    return filter(blacklisting, os.listdir('/sys/class/net'))
'''
def get_interfaces_linux():
    is_physical = lambda i: os.path.isdir('/sys/class/net/{}/device'.format(i))
    return filter(is_physical, os.listdir('/sys/class/net'))

def check_virtualization():
    command_exist = lambda fpath: os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    if os.getuid() == 0 and command_exist('/usr/sbin/virt-what'):
        proc = subprocess.Popen('/usr/sbin/virt-what',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        
        (stdout, stderr) = proc.communicate()
        
        if stdout != '' or stderr != '':
            return True

    return False

def create_interfaces_configurator():
    config = ConfigParser.SafeConfigParser()
    
    '''Remove last created files'''
    for fname in filter (lambda fname: 'network-' in fname, os.listdir('network')):
        os.remove('network/{}'.format(fname))

    '''Do not consider "lo" interface and interface without physical addr (virtual)'''
    for iface in get_interfaces_linux():
        fname = 'network/network-{}.cfg'.format(iface)
        shutil.copyfile('network/network.cfg', fname)

        config.read(fname)    
        config.set('DEFAULT', 'interface', iface)    
        if iface == get_default_gateway_linux():
            config.set('DEFAULT', 'default_gw', '(default)')
            config.set('config', 'hide', str(False))
            
        with open(fname, 'wb') as f:
            config.write(f)

        yield fname

try:
    if check_virtualization():    
        print("Unable to change MAC addr on virtualized systems: {}".format(stdout))
        sys.exit(1)
        
    map(print, create_interfaces_configurator())
except Exception as inst:
    print("Unable to set up network interfaces: {}".format(inst), sys.stderr)
    sys.exit(1)
