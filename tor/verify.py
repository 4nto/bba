'''Verify if Tor is up and properly configured'''
from __future__ import print_function
import sys

conf = ['VirtualAddrNetwork 10.192.0.0/10',
        'TransPort 9040',
        'DNSPort 53',
        'AutomapHostsOnResolve 1']

def verify():    
    with open('/etc/default/tor') as file:
        result = filter(lambda line: 'RUN_DAEMON="yes"' in line, file) == []

    if result:
        print("Module not properly configured\n")
        print("Please add the following to your \"/etc/default/tor\" and restart the service:\n", file=sys.stderr)
        print('RUN_DAEMON="yes"\n', file=sys.stderr)
        sys.exit(1)
    
    with open('/etc/tor/torrc') as file:
        def check_lines(line):
            map(conf.remove, filter(lambda c: c in line, conf))   

        map(check_lines, file)
            
    if conf:
        print("Module not properly configured\n")
        print("Please add the following to your \"/etc/tor/torrc\" and restart the service:\n", file=sys.stderr)
        map(lambda c: sys.stderr.write(c + '\n'), conf)    
        sys.exit(1)

try:
    verify()
except KeyboardInterrupt:
    print("Unable to verify module configuration\n")
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    sys.exit(1)
except Exception as inst:
    print("Unable to verify module configuration\n")
    print("Unknown error during verification: {}\n".format(inst), file=sys.stderr)
    sys.exit(1)
