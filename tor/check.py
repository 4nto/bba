'''Get from the webpage if you are using Tor'''

import re
import sys
import urllib2

SIGINT_RECEIVED = "SIGINT received (timeout or CTRL+C)", 2
NO_CONNECTION = "Unable to retrieve URL ", 3
UNKNOWN_ERROR = "Unknown error: ", 4

url = 'https://check.torproject.org/?lang=en_US'
pattern = re.compile (r'[0-9]+(?:\.[0-9]+){3}', re.I)
checkline = lambda line: 'Congratulations. This' in line

def check():    
    result = urllib2.urlopen(url)
    lines = result.readlines()
    IPline = filter(lambda line: "IP address" in line, lines)
    IP = pattern.search(IPline[0]).group() if len(IPline) == 1 else 'n/a'
    sys.stdout.write(IP)    
    return 0 if filter (checkline, lines) != [] else 1

try:
    sys.exit(check())
except KeyboardInterrupt:
    sys.stderr.write(SIGINT_RECEIVED[0])
    sys.exit(SIGINT_RECEIVED[1])
except (urllib2.HTTPError, urllib2.URLError):
    sys.stderr.write(NO_CONNECTION[0] + url)
    sys.exit(NO_CONNECTION[1])    
except Exception as inst:
    sys.stderr.write(UNKNOWN_ERROR[0] + str(inst))
    sys.exit(UNKNOWN_ERROR[1])
