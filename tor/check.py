'''Get from the webpage if you are using Tor'''

import re
import sys
import urllib2

sys.path.append('.') 
from util.configuration import Configurator

config = Configurator('tor/tor.cfg')

def check():
    pattern = re.compile (r'[0-9]+(?:\.[0-9]+){3}', re.I)
    result = urllib2.urlopen(config.get('config', 'url'))
    lines = result.readlines()
    IPline = filter(lambda line: "IP address" in line, lines)
    IP = pattern.search(IPline[0]).group() if len(IPline) == 1 else 'n/a'
    sys.stdout.write(IP)
    if filter (lambda line: 'Congratulations. This' in line, lines) == []:
        config.exit_with_error('ko')

try:
    check()
except KeyboardInterrupt:
    config.exit_with_error('sigint_received')
except (urllib2.HTTPError, urllib2.URLError):
    config.exit_with_error('no_connection')
except Exception as inst:
    config.exit_with_error('unknown_error')
